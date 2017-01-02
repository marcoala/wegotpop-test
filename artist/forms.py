from decimal import Decimal as D
from wtforms import Form, validators, DecimalField, IntegerField, SelectField


class ArtistsForm(Form):
    """ This form provide validation logic for the artist rearch endpoint
    """
    age_max = IntegerField(
        label=u'Maximum age',
        validators=[
            validators.NumberRange(min=16, max=74),
            validators.Optional()
        ]
    )
    age_min = IntegerField(
        label=u'Minimum age',
        validators=[
            validators.NumberRange(min=16, max=74),
            validators.Optional()
        ]
    )
    location_latitude = DecimalField(
        label=u'Location latitude',
        places=6,
    )
    location_longitude = DecimalField(
        label=u'Location longitude',
        places=6,
    )
    location_radius = DecimalField(
        label=u'Location radius',
        places=2,
    )
    rate_max = DecimalField(
        label=u'Max rate',
        places=2,
        validators=[
            validators.NumberRange(min=D('10.00'), max=D('39.97')),
            validators.Optional()
        ]
    )
    gender = SelectField(
        label=u'Gender',
        choices=[('F', 'Female'), ('M', 'Male')],
        validators=[
            validators.Optional()
        ]
    )
