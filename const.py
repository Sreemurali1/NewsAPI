TOP_HEADLINES_URL = "https://newsapi.org/v2/top-headlines"
EVERYTHING_URL = "https://newsapi.org/v2/everything"
SOURCES_URL = "https://newsapi.org/v2/sources"


#: The 2-letter ISO 3166-1 code of the country you want to get headlines for.  If not specified,
#: the results span all countries.
COUNTRIES = [
    "ae", "ar", "at", "au", "be", "bg", "br", "ca", "ch", "cn", "co", "cu", "cz",
    "de", "eg", "fr", "gb", "gr", "hk", "hu", "id", "ie", "il", "in", "it", "jp",
    "kr", "lt", "lv", "ma", "mx", "my", "ng", "nl", "no", "nz", "ph", "pl", "pt",
    "ro", "rs", "ru", "sa", "se", "sg", "si", "sk", "th", "tr", "tw", "ua", "us",
    "ve", "za"
]



#: The 2-letter ISO-639-1 code of the language you want to get articles for.  If not specified,
#: the results span all languages.
LANGUAGES = [
    "ar", "de", "en", "es", "fr", "he", "it", "nl", "no", "pt", "ru", "sv", "ud", "zh"
]

get_LANGUAGES = ["en"]

#: The category you want to get articles for.  If not specified,
#: the results span all categories.
CATEGORIES = {"business", "entertainment", "general", "health", "science", "sports", "technology"}

#: The order to sort article results in.  If not specified, the default is ``"publishedAt"``.
SORT_METHOD = {"relevancy", "popularity", "publishedAt"}