Introduction
============

Closed sections
---------------

This products is intended to solve the use case for "closed sections", which
are described as "sections for which a subscription is necessary". 
This is rather a broad issue, and as is often the case, the details will
probably be filled in later, but i'm sure the use case will sound familiar to a
lot of people.

The standard Plone functionality does a good job: making folder private takes
care of security, and it's easy to share the folder with a user (or group).

What's missing for the use case is, in my opinion:

    - a way for Managers to mark certain folders as being a "closed section"
    - for Members, a list of subscribable "sections"
    - * a mechanism for users to request a "subscription"
      * a way for Managers to approve subscriptions
    - a list of users's "subscriptions"

These are all fairly minor things, which should work easily with Plone's
functionality.

It seems there's nothing around yet that works for Plone 4 (we're targeting
4.2). I've looked at collective.groupspaces.* briefly, but it looks too big.
collective.groupspaces.content adds a content type (subclasses ATFolder), which
i don't like. And it appears not to work for Plone 4, though i haven't tried
installing it yet.

Implementation
--------------

We have these User Stories, and suggested implementations:

    1. [V] Mark as Subscribable: solve by sticking an extra interface on a
       Folder, possibly use p4a.subtyper

    2. [V] List of Subscribable Sections: create a Portlet

    3.  a. [V] Request a subscription: View + Annotation storage on the 
           Folder

        b. i.  [ ] List subscription requests in a Portlet

           ii. [W] Manage requests from View on Folder 

    4. [W ] List of Member's subscriptions: a View.

    5. [ ] Custom Workflow (one state, maybe change display name to 
           "Subscription required".

    6. [V] Custom "Insufficient privileges" message: When trying to view a 
           "Closed Section", display a different message. Link to subscription 
           request View.

    7. a. [ ] Remove own subscription request:
       b. [ ] Remove own subscription (protected by extra click):

    8. [W] Get view permission when subscription is granted: Grant Member
           the `Reader` Role on the Folder 
           a. [ ] after subscription approval on a Closed Section
           b. [V] immediately after request on an Open Section 

| [V]: done
| [ ]: open
| [W]: work in progress

Open sections
-------------

In addition, there is also a use case for "Open sections". These work in the
same way, except that after a subscription request, subscription is granted
immediately.

Issues
======

A list of issues per User Story:

2. p4a.subtyper doesn't re-index the object after it alters its interfaces, so
   the list of Subscribable Section Folders in the portlet isn't updated until 
   someone changes the folders or updates the catalog.
