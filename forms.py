from wtforms import Form, TextField, validators, HiddenField
from wtforms.fields.html5 import EmailField
from models import UserEmail
def leght_honeypot(form, field):
    if len(field.data)>0:
        raise validators.ValidationError('This field is must be null')

class Query(Form):
    
    autor = TextField('Autor: ', [validators.Required(message='This field is required')],default='S. J. Pan and Q. Yang')

    title = TextField('Title: ', [validators.Required(message='This field is required')],default='A survey on transfer learning')

    year = TextField('Year: ', [validators.Required(message='This field is required')],default='2010')

    honeypot = HiddenField('',[leght_honeypot])

class Subscribe(Form):

    email = EmailField('Email address: ',
        [
            validators.Required(message='This field is required'),
            validators.Email(message='Email format not valid')
        ]
    )

    honeypot = HiddenField('',[leght_honeypot])


    def validate_email(self, field):
        correo_field = field.data
        user = UserEmail.get_by_email(correo_field)
        if user is not None:
            raise validators.ValidationError('The email address provided is already registrer. Wait for contact please.')

        des = len(field.data)
        if des > 50:
            error = 'The email must content 50 chars max. And provided email contains: {}'.format(des)
            raise validators.ValidationError(error)
