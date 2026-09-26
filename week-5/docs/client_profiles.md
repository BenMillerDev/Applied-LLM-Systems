## Client Profiles

Client profiles in NailSalonApp are not something an owner fills out -- they're built automatically from booking history. The useClients hook scans every appointment tied to a given client's email address and aggregates it into a profile, so a client's history exists the moment they've booked once, with no separate "add a client" step anywhere in the app.

Each generated profile shows a client's total number of visits, their total lifetime spend, which services they book most often, and a computed fill due date that estimates when they're likely due for their next appointment based on their past booking pattern.

Owners can also attach free-form notes to a client -- reminders about a preference, an allergy, or anything else worth remembering. Those notes aren't stored on the appointment record itself; they live in a separate clientNotes collection, keyed by a combination of the owner's id and the client's email, so a note persists independently even if every appointment tied to that client were ever deleted.

