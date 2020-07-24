
DOCUMENTATION:

Enter 'exit' at "username","UCS IP", or "password" prompt to exit program

File path should be formatted, for example as, '/folder/huu.iso'.

Supports only the following file sharing protocols: nfs,cifs,www. I recommend using free software FreeNAS, and/or HFS (HTTP File Server). Dedicated NAS is ideal.

If connection to server fails before update attempt sent, its entry will be deleted as to not disrupt the update process for other servers in list.

The update monitoring function does not run in order nor does it identify the server being monitored, this can be developed further in the future.

WARNING: May encounter problems with older CIMC versions i.e 1.47/1.5

Coded by clmoss@cisco.com (Clayton M. Moss)

Please contact clmoss@cisco.com if any bugs are encountered, or for feature requests. I plan to add features in the future.
