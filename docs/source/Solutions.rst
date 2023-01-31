Solutions to Common Problems
============================

While the software itself is COMPLETELY flawless, the user may run into issues that are their OWN fault and do not reflect at all on any (nonexistent) mistakes made by the designers of this package. Here are some solutions to these problems:

#. **HTTP500 error: astroquery does not recognize the given input name**

     If this occurs, it is reccommended to download the desired JWST fits files from https://mast.stsci.edu/portal/Mashup/Clients/Mast/Portal.html
     and set query to False within the make_image() function.

#. **list index out of range**

    This will occur if the query failed to find any data that matched the object name, please follow the steps above to resolve this.

#. **Mast token required for querying**

    This requires a user profile on MAST to resolve. For more information, please visit: https://auth.mast.stsci.edu/info 