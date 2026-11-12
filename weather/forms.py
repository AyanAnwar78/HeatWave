from django import forms


class CitySearchForm(forms.Form):
    city = forms.CharField(
        max_length=100,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search city…",
            "class": (
                "w-full bg-white/10 backdrop-blur border border-white/20 "
                "text-white placeholder-white/50 rounded-xl px-5 py-3 "
                "focus:outline-none focus:ring-2 focus:ring-orange-400 "
                "text-sm transition"
            ),
            "autocomplete": "off",
        }),
    )

