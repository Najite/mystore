from django import forms

PRODUCT_QUANTITY = [(i, str(i)) for i in range(1,20)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(coerce=int,
                                      choices=PRODUCT_QUANTITY)
    override = forms.BooleanField(initial=False,
                                  required=False,
                                  widget=forms.HiddenInput)
    
    