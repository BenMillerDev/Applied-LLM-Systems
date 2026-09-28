## Authentication and User Data

Owners can sign up and log in either with a plain email and password or with Google sign-in; the signup screen is where a brand-new owner account gets created, separate from the login screen used afterward. Auth state for the whole app is tracked through a single AuthContext, and the app's root layout automatically redirects any signed-out user back to the login screen, so no individual screen has to check auth state itself.

Google sign-in has one wrinkle: the real native Google sign-in flow doesn't work inside Expo Go, the sandboxed app used for development and testing. To work around that, a mock version of the Google sign-in flow is swapped in automatically whenever the app detects it's running in Expo Go, so development and testing aren't blocked by a flow that only works in a fully built app.

Each owner's account is stored in Firestore under a users collection, keyed by their Firebase uid. That record holds their email, their name, their salon's name, their phone number, a role field, and the timestamp their account was created -- everything the rest of the app needs to know about who's logged in without a second lookup.
