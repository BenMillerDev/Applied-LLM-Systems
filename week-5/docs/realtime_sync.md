## Real-Time Updates

The owner side of the app avoids one-time data reads wherever a screen needs to reflect what's currently true. The dashboard and appointment list both use Firestore's onSnapshot listeners instead, through a shared useAppointments hook, so the underlying data is pushed to the app the moment it changes rather than being fetched on a timer or on screen load.

In practice this means that when a customer finishes a booking on the web app, the appointment shows up on the owner's dashboard and appointments screen immediately, with no pull-to-refresh or manual reload needed. The same listener-based hook backs every appointment-related screen, so the real-time behavior is consistent across the whole owner app rather than being implemented separately per screen.

