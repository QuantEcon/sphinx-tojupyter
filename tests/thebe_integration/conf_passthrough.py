# Configuration with tojupyter_drop_raw_html = False
# This simulates the old behavior where raw HTML passes through

project = 'Thebe Integration Test - Passthrough Mode'
author = 'Test'
release = '1.0'

extensions = ['sphinx_tojupyter']

tojupyter_default_lang = "python3"
tojupyter_kernels = {
    "python3": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python3",
            "name": "python3"
        },
        "file_extension": ".py",
    }
}

# Set to False to allow raw HTML passthrough (old behavior)
tojupyter_drop_raw_html = False
