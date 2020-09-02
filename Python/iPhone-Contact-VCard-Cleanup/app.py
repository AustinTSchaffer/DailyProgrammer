import vobject
from io import FileIO

contacts = open('data/iCloud Contacts.vcf', mode='r')

comps = vobject.readComponents(contacts)
fixed_contacts = []

for comp in comps:
    fn = comp.fn.value.split(' ')
    fn = str.join(' ', fn[1:] + fn[:1])
    comp.fn.value = fn
    fixed_contacts.append(comp)
    print(comp.serialize())
