## Customer Booking Flow

The booking experience a customer actually sees lives entirely in a separate React web app, hosted on Firebase and reachable from any device with just a link -- no account, no app install, and no password to remember. It's designed to work the same whether a client opens it on their phone from a text message or on a laptop.

Booking happens in four steps, tracked visually by a shared progress bar component so the customer always knows how much is left: first, selecting a service along with any add-ons, nail shape, and nail length; second, picking a date from the ones the owner has available; third, picking a specific time slot on that date; and fourth, entering contact information to confirm the booking.
Only dates and times the owner has actually marked as available make it into the date and time pickers in the first place -- the filtering happens before the customer ever sees the calendar, so there's no way to select a slot that's already taken or outside the owner's hours. Once submitted, a confirmation screen shows the customer a full summary of what they just booked.
