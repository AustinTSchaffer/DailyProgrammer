# iCloud Contacts Cleanup

This short Python script swaps the first name and the last name of all of the
contacts in a vCard file (`.vcf`). 

## Installation

The only requirement of this short script is 
[`vobject`](https://pypi.org/project/vobject/), but there is an included
requirements.txt just in case.

```bash
# source venv/bin/activate
pip install -r requirements.txt
```

## Usage

This script reads the file `data/iCloud Contacts.vcf` and then dumps the
fixed contacts to the console. Redirect the output into something resembling
`data/fixed contacts.vcf` to save the results.

## Background

This script was written because I had decided to flip a switch on my iPhone 
at one point, which caused all of my contacts to have their names backwards 
when I exported them out of iCloud contacts and imported them into Google 
Contacts.

Google Contacts has an option to delete a recent contacts import, so I did
that, tried a few more settings in iCloud Contacts, reimported them into
Google Contacts, still had the same issue, etc.

I wrote this script, which cleaned up the exported iCloud contacts, before 
importing them into Google Contacts. This fixed the backwards names, but now
I had some duplicated contacts from the last time I switched from Android to
iPhone. Google Contacts has an option to auto-merge duplicated contacts by
name, which seemed to work.

Never be afraid to switch to a different provider, you can usually take your
stuff with you.

