import os
import warnings
from django.utils.translation import ugettext_lazy as _
from os.path import dirname
import csv

warnings.simplefilter('error', DeprecationWarning)

BASE_DIR = dirname(dirname(dirname(dirname(os.path.abspath(__file__)))))
CONTENT_DIR = os.path.join(BASE_DIR, 'content')

SECRET_KEY = 'NhfTvayqggTBPswCXXhWaN69HuglgZIkM'

DEBUG = True
ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'accounts.CustomUser'

SITE_ID = 1

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    #'grappelli, (if present)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_forms_bootstrap',
    'datetimepicker',

    # Vendor apps
    'bootstrap4',
    'crispy_forms',

    # Application apps
    'main',
    'accounts',
    'event',
    'search',
    'calendars',
    'user_profile',
    'career_fair',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(CONTENT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(CONTENT_DIR, 'tmp/emails')
EMAIL_HOST_USER = 'test@example.com'
DEFAULT_FROM_EMAIL = 'test@example.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ATOMIC_REQUESTS': True,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

ENABLE_USER_ACTIVATION = True
DISABLE_USERNAME = False
LOGIN_VIA_EMAIL = True
LOGIN_VIA_EMAIL_OR_USERNAME = False
LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'accounts:log_in'
USE_REMEMBER_ME = True

RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME = False
ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE = True

RECRUITER_FIELDS = ['company'] 
STUDENT_FIELDS = ['university']
PROFILE_SIGN_UP = ['user_type','username', 'first_name', 'last_name', 'email', 'password1', 'password2'] # add user_type
SIGN_UP_FIELDS = ['first_name', 'last_name', 'email', 'password1', 'password2'] # add user_type
UNIV_LIST = [
'Harvard University',
'Massachusetts Institute of Technology',
'Stanford University',
'California Institute of Technology',
'Princeton University',
'Yale University',
'Columbia University',
'University of California, Berkeley',
'University of Chicago',
'Cornell University',
'University of Pennsylvania',
'Johns Hopkins University',
'University of California, Los Angeles',
'University of California, San Diego',
'Rockefeller University',
'New York University',
'University of California, San Francisco',
'University of Wisconsin - Madison',
'University of Illinois at Urbana - Champaign',
'Duke University',
'University of Texas Southwestern Medical Center',
'University of Texas at Austin',
'Northwestern University',
'University of Michigan, Ann Arbor',
'University of North Carolina at Chapel Hill',
'Washington University in St. Louis',
'University of Utah',
'University of Washington - Seattle',
'University of California, Santa Barbara',
'Purdue University, West Lafayette',
'Pitzer College',
'Carnegie Mellon University',
'University of Southern California',
'University of California, Davis',
'University of Colorado Boulder',
'University of California, Irvine',
'University of Minnesota, Twin Cities',
'University of Arizona',
'Ohio State University, Columbus',
'University of Rochester',
'University of Florida',
'Rice University',
'Dartmouth College',
'Vanderbilt University',
'Boston University',
'Pennsylvania State University, University Park',
'Brown University',
'University of Maryland, College Park',
'University of Pittsburgh - Pittsburgh Campus',
'Rutgers University-New Brunswick',
'Texas A&M University, College Station',
'Case Western Reserve University',
'Arizona State University',
'Emory University',
'University of Virginia',
'Tufts University',
'Georgia Institute of Technology',
'Williams College',
'University of Texas MD Anderson Cancer Center'
]

MAJOR_LIST = [
 'General Agriculture',
 'Agriculture Production And Management',
 'Agricultural Economics',
 'Animal Sciences',
 'Food Science',
 'Plant Science And Agronomy',
 'Soil Science',
 'Miscellaneous Agriculture',
 'Forestry',
 'Natural Resources Management',
 'Fine Arts',
 'Drama And Theater Arts',
 'Music',
 'Visual And Performing Arts',
 'Commercial Art And Graphic Design',
 'Film Video And Photographic Arts',
 'Studio Arts',
 'Miscellaneous Fine Arts',
 'Environmental Science',
 'Biology',
 'Biochemical Sciences',
 'Botany',
 'Molecular Biology',
 'Ecology',
 'Genetics',
 'Microbiology',
 'Pharmacology',
 'Physiology',
 'Zoology',
 'Neuroscience',
 'Miscellaneous Biology',
 'Cognitive Science And Biopsychology',
 'General Business',
 'Accounting',
 'Actuarial Science',
 'Business Management And Administration',
 'Operations Logistics And E-Commerce',
 'Business Economics',
 'Marketing And Marketing Research',
 'Finance',
 'Human Resources And Personnel Management',
 'International Business',
 'Hospitality Management',
 'Management Information Systems And Statistics',
 'Miscellaneous Business & Medical Administration',
 'Communications',
 'Journalism',
 'Mass Media',
 'Advertising And Public Relations',
 'Communication Technologies',
 'Computer And Information Systems',
 'Computer Programming And Data Processing',
 'Computer Science',
 'Information Sciences',
 'Computer Administration Management And Security',
 'Computer Networking And Telecommunications',
 'Mathematics',
 'Applied Mathematics',
 'Statistics And Decision Science',
 'Mathematics And Computer Science',
 'General Education',
 'Educational Administration And Supervision',
 'School Student Counseling',
 'Elementary Education',
 'Mathematics Teacher Education',
 'Physical And Health Education Teaching',
 'Early Childhood Education',
 'Science And Computer Teacher Education',
 'Secondary Teacher Education',
 'Special Needs Education',
 'Social Science Or History Teacher Education',
 'Teacher Education: Multiple Levels',
 'Language And Drama Education',
 'Art And Music Education',
 'Miscellaneous Education',
 'Library Science',
 'Architecture',
 'General Engineering',
 'Aerospace Engineering',
 'Biological Engineering',
 'Architectural Engineering',
 'Biomedical Engineering',
 'Chemical Engineering',
 'Civil Engineering',
 'Computer Engineering',
 'Electrical Engineering',
 'Engineering Mechanics Physics And Science',
 'Environmental Engineering',
 'Geological And Geophysical Engineering',
 'Industrial And Manufacturing Engineering',
 'Materials Engineering And Materials Science',
 'Mechanical Engineering',
 'Metallurgical Engineering',
 'Mining And Mineral Engineering',
 'Naval Architecture And Marine Engineering',
 'Nuclear Engineering',
 'Petroleum Engineering',
 'Miscellaneous Engineering',
 'Engineering Technologies',
 'Engineering And Industrial Management',
 'Electrical Engineering Technology',
 'Industrial Production Technologies',
 'Mechanical Engineering Related Technologies',
 'Miscellaneous Engineering Technologies',
 'Materials Science',
 'Nutrition Sciences',
 'General Medical And Health Services',
 'Communication Disorders Sciences And Services',
 'Health And Medical Administrative Services',
 'Medical Assisting Services',
 'Medical Technologies Technicians',
 'Health And Medical Preparatory Programs',
 'Nursing',
 'Pharmacy Pharmaceutical Sciences And Administration',
 'Treatment Therapy Professions',
 'Community And Public Health',
 'Miscellaneous Health Medical Professions',
 'Area Ethnic And Civilization Studies',
 'Linguistics And Comparative Language And Literature',
 'French German Latin And Other Common Foreign Language Studies',
 'Other Foreign Languages',
 'English Language And Literature',
 'Composition And Rhetoric',
 'Liberal Arts',
 'Humanities',
 'Intercultural And International Studies',
 'Philosophy And Religious Studies',
 'Theology And Religious Vocations',
 'Anthropology And Archeology',
 'Art History And Criticism',
 'History',
 'United States History',
 'Cosmetology Services And Culinary Arts',
 'Family And Consumer Sciences',
 'Military Technologies',
 'Physical Fitness Parks Recreation And Leisure',
 'Construction Services',
 'Electrical, Mechanical, And Precision Technologies And Production',
 'Transportation Sciences And Technologies',
 'Multi/Interdisciplinary Studies',
 'Court Reporting',
 'Pre-Law And Legal Studies',
 'Criminal Justice And Fire Protection',
 'Public Administration',
 'Public Policy',
 'Physical Sciences',
 'Astronomy And Astrophysics',
 'Atmospheric Sciences And Meteorology',
 'Chemistry',
 'Geology And Earth Science',
 'Geosciences',
 'Oceanography',
 'Physics',
 'Multi-Disciplinary Or General Science',
 'Nuclear, Industrial Radiology, And Biological Technologies',
 'Psychology',
 'Educational Psychology',
 'Clinical Psychology',
 'Counseling Psychology',
 'Industrial And Organizational Psychology',
 'Social Psychology',
 'Miscellaneous Psychology',
 'Human Services And Community Organization',
 'Social Work',
 'Interdisciplinary Social Sciences',
 'General Social Sciences',
 'Economics',
 'Criminology',
 'Geography',
 'International Relations',
 'Political Science And Government',
 'Sociology',
 "Miscellaneous Social Sciences"]
if DISABLE_USERNAME:
    SIGN_UP_FIELDS = ['first_name', 'last_name', 'email', 'password1', 'password2']

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
    ('zh-Hans', _('Simplified Chinese')),
]

TIME_ZONE = 'US/Pacific'
USE_TZ = True

STATIC_ROOT = os.path.join(CONTENT_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(CONTENT_DIR, 'media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(CONTENT_DIR, 'assets'),
]

LOCALE_PATHS = [
    os.path.join(CONTENT_DIR, 'locale')
]
