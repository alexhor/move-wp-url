import os, regex

def replace_sql(content, orig_url, new_url, orig_path, new_path, https, www):
    """replace an url with a new url in the given string

    >>> content = open("test.sql", "r").read()
    >>> print(replace_sql(content, "uscfr.de", "uscfr.h-software.de", "/www.uscfr.de", "/var/www/vhosts/h-software.de/uscfr.h-software.de", True, False))
    https://uscfr.h-software.de
    https://uscfr.h-software.de
    <BLANKLINE>
    https://uscfr.h-software.de
    https://uscfr.h-software.de
    <BLANKLINE>
    /var/www/vhosts/h-software.de/uscfr.h-software.de/wp-content/uploads/2017/05/Eckert_2012-150x150.jpg
    \\\\/var\\\\/www\\\\/vhosts\\\\/h-software.de\\\\/uscfr.h-software.de\\\\/wp-content\\\\/uploads\\\\/2017\\\\/05\\\\/Eckert_2012-150x150.jpg
    <BLANKLINE>
    https:\\\\/\\\\/uscfr.h-software.de
    https:\\\\/\\\\/uscfr.h-software.de
    <BLANKLINE>
    https:\\\\/\\\\/uscfr.h-software.de
    https:\\\\/\\\\/uscfr.h-software.de
    <BLANKLINE>
    https%3A%2F%2Fuscfr.h-software.de
    https%3A%2F%2Fuscfr.h-software.de
    <BLANKLINE>
    https%3A%2F%2Fuscfr.h-software.de
    https%3A%2F%2Fuscfr.h-software.de
    """
    # convert all http to https and strip a possible www
    content = regex.sub(r"http://(?:www.)?" + orig_url, "https://" + orig_url, content)
    content = regex.sub(r"http:\\\\/\\\\/(?:www.)?" + orig_url, "https:\\\\\\\\/\\\\\\\\/" + orig_url, content)
    content = regex.sub(r"http%3A%2F%2F(?:www.)?" + orig_url, "https%3A%2F%2F" + orig_url, content)

    # strip all remaining www from the original url
    content = regex.sub(r"https://www." + orig_url, r"https://" + orig_url, content)
    content = regex.sub(r"https:\\\\/\\\\/www." + orig_url, "https:\\\\\\\\/\\\\\\\\/" + orig_url, content)
    content = regex.sub(r"https%3A%2F%2Fwww." + orig_url, "https%3A%2F%2F" + orig_url, content)
    
    # replace directory names
    if orig_path != False and new_path != False:
        escaped_orig_path =regex.sub(r"/", r"\\\\\\\\/", orig_path)
        escaped_new_path =regex.sub(r"/", r"\\\\\\\\/", new_path)
        content = regex.sub(r"(?<!https:/|https:\\\\/\\\\)" + escaped_orig_path, escaped_new_path, content)
        content = regex.sub(r"(?<!https:/|https:\\\\/\\\\)" + orig_path, new_path, content)

    # check which protocol to use for the new url
    if https:
        protocol = "https"
    else:
        protocol = "http"

    # check if www. should be used for the new url
    if www:
        www = "www."
    else:
        www = ""
    
    # replace url names (new_url should have www)
    content = regex.sub(r"https://" + orig_url, "" + protocol + "://" + www + new_url, content)
    content = regex.sub(r"https:\\\\/\\\\/" + orig_url, "" + protocol + ":\\\\\\\\/\\\\\\\\/" + www + new_url, content)
    content = regex.sub(r"https%3A%2F%2F" + orig_url, "" + protocol + "%3A%2F%2F" + www + new_url, content)

    # remove all remaining www.
    content = regex.sub(r"www." + orig_url, orig_url, content)
    
    # replace all remaining matches literaly
    content = regex.sub(r"" + orig_url, www + new_url, content)

    # return the processed content
    return content


def main():
    """run url replacement once"""
    # create an output folder if it doesn't exist yet
    try:
        os.mkdir('output')
    except OSError:
        pass

    # get all required data from the user
    orig_url = input("Which url should be replaced? (without www. please) ")
    new_url = input("Which url should be used instead? (without www. please) ")
    https_str = input("Should HTTPS be used? ")
    https = (https_str == "yes" or https_str == "y" or https_str == "Yes" or https_str == "Y")
    www_str = input("Should www. be used? (for the new url) ")
    www = (www_str == "yes" or www_str == "y" or www_str == "Yes" or www_str == "Y")
    replace_paths_str = input("Should paths be replaced? ")
    replace_paths = (replace_paths_str == "yes" or replace_paths_str == "y" or replace_paths_str == "Yes" or replace_paths_str == "Y")
    if replace_paths:
        orig_path = input("What was the old path? (relative, with leading and without trailing slash please) ")
        new_path = input("What is the new path? (relative, with leading and without trailing slash please) ")
    else:
        new_path = orig_path = False

    # check every file in the current directory
    for file in os.listdir():
        # skip testing file
        if file == "test.sql":
            continue
        # get all sql files
        if(file[-4:] == '.sql'):
            # load the files content
            file_content = open(file, "r", encoding="utf-8").read()
            # replace the url
            new_content = replace_sql(file_content, orig_url, new_url, orig_path, new_path, https, www)
            # save the new sql expression to a new file
            new_file = open("output/" + file, "w", encoding="utf-8")
            new_file.write(new_content)
            new_file.close()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()
