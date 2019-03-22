from flask_user.forms import RegisterForm
from flask_wtf import Form, FlaskForm
from wtforms import *
# from wtforms.validators import DataRequired, Email
from flask import current_app as app
from flask_user import current_user
from models import *
from flask_sqlalchemy import SQLAlchemy
from wtforms_alchemy import model_form_factory, ModelFieldList, ModelFormField, QuerySelectMultipleField, QuerySelectField
from wtforms.compat import with_metaclass, iteritems, itervalues

BaseModelForm = model_form_factory(Form)
db = SQLAlchemy(app)

def unique_email_validator(form, field):
    """ Username must be unique. This validator may NOT be customized."""
    user_manager =  app.user_manager
    if not user_manager.email_is_available(field.data):
        raise ValidationError(('This email is already in use. If you have registered, but not created a password, please use the "Forgot Password" link.'))

class CustomRegisterForm(RegisterForm):
    """Register new user form."""
    email = StringField(('Email'), validators=[
        validators.DataRequired(('Email is required')),
        validators.Email(('Invalid Email')),
        unique_email_validator])

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

    def populate_obj(self, obj):
        """
        Populates the attributes of the passed `obj` with data from the form's
        fields.

        :note: This is a destructive operation; Any attribute with the same name
               as a field will be overridden. Use with caution.
        """
        for name, field in iteritems(self._fields):
            field.populate_obj(obj, name)

class ModelFieldList(FieldList):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model", None)
        super(ModelFieldList, self).__init__(*args, **kwargs)
        if not self.model:
            raise ValueError("ModelFieldList requires model to be set")

    def validate(self, form, extra):
        for entry in self.entries:
            print(entry)
            if super(ModelFieldList, self).validate(entry) is False:
              return False
        if self.model == User:
            emaillist = []
            for user in form.users:
                if not user.email.data:
                    # if there is no email, skip the rest
                    user.email.data = None
                    continue
                if user.email.data in emaillist:
                    # if the email shows up more than once in the form throw an error
                    form.users.errors.append('Email is not unique')
                    return False
                emaillist.append(user.email.data)
                if user.object_data and user.object_data.email != user.email.data:
                    # if the email changed, see if it already exists
                    if db.session.query(User).filter_by(email = user.email.data).first():
                        form.users.errors.append('Email is not unique')
                        return False
        return True

class QueryMultiCheckboxField(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

    def _get_data(self):
        raise(AttributeError)
        formdata = self._formdata
        if formdata is not None:
            data = []
            for pk, obj in self._get_object_list():
                if not formdata:
                    break
                elif pk in formdata:
                    formdata.remove(pk)
                    data.append(obj)
            if formdata:
                self._invalid_formdata = True
            self._set_data(data)
        return self._data

    def iter_choices(self):
        if self.allow_blank:
            yield ('__None', self.blank_text, self.data is None)

        datalist = []
        for data in self.data:
            datalist.append(data.id)

        for pk, obj in self._get_object_list():
            # raise(AttributeError)
            yield (pk, self.get_label(obj), obj.id in datalist)

    def process_formdata(self, valuelist):
        if valuelist:
            if self.allow_blank and valuelist[0] == '__None':
                self.data = None
            else:
                self._data = None
                self._formdata = valuelist

    def populate_obj(self, obj, name):
        if name == 'communications':
            # obj.communications = []
            if obj.communications != self.data:
                for comm in obj.communications:
                    if comm not in self.data:
                        # raise(AttributeError)
                        obj.communications.pop()
                    else:
                        raise(AttributeError)

                for comm in self.data:
                    objsession = db.session.object_session(obj)
                    if objsession:
                        obj.communications.append(objsession.query(Communication).filter_by(id = comm.id).one())
                    else:
                        obj.communications.append(comm)
        else:
            super(QuerySelectMultipleField, self).populate_obj(obj, name)

class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ['active']
        unique_validator = None

class CommunicationForm(ModelForm):
    class Meta:
        model = Communication

class RegistrationForm(ModelForm):
    class Meta:
        model = Household
    commquery = db.session.query(Communication).filter_by(display = True).order_by('name').all
    users = ModelFieldList(ModelFormField(UserForm), model = User)
    communications = QueryMultiCheckboxField('Label', query_factory = commquery, get_label = 'name')
