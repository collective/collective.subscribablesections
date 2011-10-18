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

    1. a way for Managers to mark certain folders as being a "closed section"
    2. for Members, a list of subscribable "sections"
    3.  a. a mechanism for users to request a "subscription"
        b. a way for Managers to approve subscriptions
    4. a list of users's "subscriptions"

More may follow, of course.

These are all fairly minor things, which should work easily with Plone's
functionality.

My currents thoughts for solutions are:

    1. solve by sticking an extra interface on a Folder, possibly use 
       p4a.subtyper
    2. create a view + portlet
    3.  a. annotate on the folder
        b. create a portlet which lists subscription requests, view for 
           approving
    4. portlet
    5. perhaps a custom workflow
    6. when trying to view a "Closed Section", display a message to request a
       subscription

It seems there's nothing around yet that works for Plone 4 (we're targeting
4.2). I've looked at collective.groupspaces.* briefly, but it looks too big.
collective.groupspaces.content adds a content type (subclasses ATFolder), which
i don't like. And it appears not to work for Plone 4, though i haven't tried
installing it yet.

Open sections
-------------

In addition, there is also a use case for "Open sections". These in the same
way, but after a subscription request, subscription is granted immediately.
