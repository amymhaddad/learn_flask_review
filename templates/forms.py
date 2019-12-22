from flask_wtf import Form

from wtforms import StringField
from flask_wtf.html5 import URLField
from wtforms.validators import DataRequired, url


class BookmarkForm(Form):
    url = URLField("url", validators=[DataRequired(), url()])
    description = StringField("description")

    # overwrite the validate() method of the form class (https://wtforms.readthedocs.io/en/stable/forms.html_)
    # This method is called when we call validate_on_submit() in VF
    def validate(self):
        # Run checks to see how url starts: IF the url does NOT start with http or https, then we add it automatically
        # Ie, if user doesn't enter http or https, we will add it for them BUT they must include the top-level domain  bc that's something the url validtora checks for
        if not self.url.data.startswith("http://") or self.url.data.startswith(
            "https://"
        ):
            self.url.data = "http://" + self.url.data

        # call the validate method on the parent class. This checks all other validtors against the data. If there's an error it retursn False
        if not Form.validate(self):
            return False

        # check if user has entered a description
        # IF not, I set the description to the url, that way the descriotion is NEVER empty
        if not self.description.data:
            self.description.data = self.url.data

        # imp to do this b/c validate() MUST return a bool
        return True
