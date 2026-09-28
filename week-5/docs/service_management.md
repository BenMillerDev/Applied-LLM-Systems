## Service Management

Owners manage their service menu from a dedicated services screen, with a separate service-form screen used for both adding a new service and editing an existing one -- the same form handles both cases. All reads and writes to service data go through a single useServices hook, which wraps the underlying Firestore calls so no screen talks to Firestore directly.

Each service is stored in Firestore under the services collection, keyed by a generated serviceId. A service document carries the owning ownerId, a category, a name and description, a duration, a price, an array of optional addOns, and an isActive flag that lets an owner hide a service without deleting its history.

New owners don't start from an empty service list. The app ships with a default service catalog defined directly in the app's constants, so a newly created salon account already has a reasonable starting menu to edit rather than a blank screen. This same catalog is also what the onboarding flow points to when it prompts a new owner to review their services.