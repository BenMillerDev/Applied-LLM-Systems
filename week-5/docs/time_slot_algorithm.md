## Time Slot Algorithm

The logic that decides which appointment times are actually bookable lives in a single shared utility module used by both the owner app and the customer booking web app, so the two surfaces never disagree about what's available. Given a day, it produces the list of open slots a customer is allowed to pick from.

To build that list, the algorithm reads the owner's weekly schedule for that day, checks every existing appointment already on the books for conflicts, and inserts the owner's configured buffer time between back-to-back appointments so nothing is scheduled with zero gap. It also removes any date the owner has manually blocked, and filters out any slot that has already passed.

On top of all that, there's a fixed rule that applies no matter what the owner's settings say: a customer must book at least 1 hour in advance. Any slot that falls inside that 1-hour window from the current time is excluded from the results, even if it would otherwise be open, to avoid a booking landing on the owner's calendar with almost no notice.
