# WFM
WFM (Website File Manager) is the equivalent of Sambda  package for linux for filesharing but as a local Website that runs on your PC/Optiplex.

# How it works
*WFM* Runs on port ***2704*** by default modified by **FSConfig.conf** and saves in a **/share** directory also modifiable in the same FSConfig.

# How do i add users
**WFM** reads users accounts by going to **/configs/WFMUSER.conf** in a JSON Format:
{
 (user) : {
   caf:True,
   crf:True,
   password:(password),
   login_enabled:True
 }
}
***Meanings of the JSON***
**caf means "Can Create files" while crf means "Can Read Files"**
*Replace (user) and (password) by their actual name & password u use for their user.*

# How do i easily add a user?
**Go to (IP)/Admin** for administrator view. **Use credentials (default: ADMIN, password: ADM90!X)**
**Modify those credentials critically in */config/SA.conf* for security.**
