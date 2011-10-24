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

Open sections
-------------

In addition, there is also a use case for "Open sections". These work in the
same way, except that after a subscription request, subscription is granted
immediately.

User Stories
============

We have these User Stories, and suggested implementations:

    1. [V] Mark as Subscribable: solve by sticking an extra interface on a
       Folder, possibly use p4a.subtyper

    2. [V] List of Subscribable Sections: create a Portlet

    3.  a. [V] Request a subscription: View + Annotation storage on the 
           Folder

        b. i.  [V] List subscription requests in a Portlet

           ii. [V] Manage requests from View on Folder 

    4. [V] List of Member's subscriptions: a View.

    5. a. [ ] ??? Change display names for Open/Closed Sections
       b. [ ] ??? Give Open/Closed Sections a one-state workflow

    6. [V] Custom "Insufficient privileges" message: When trying to view a 
           "Closed Section", display a different message. Link to subscription 
           request View.

    7. a. [ ] Remove own subscription request:
       b. [ ] Remove own subscription (protected by extra click):

    8. [V] Get view permission when subscription is granted: Grant Member
           the `Reader` Role on the Folder 
           a. [V] after subscription approval on a Closed Section
           b. [V] immediately after request on an Open Section 

    9. [ ] Support for delegating more than one Role

| [V]: done
| [ ]: open
| [W]: work in progress

Getting started
===============

Marking a Folder as a Subscribable Section
------------------------------------------

After installation, you (The Manager) should see an extra button "Sub-types"
(next to "Actions") on Folders. Here, you can mark the Folder as being an
"Open" or "Closed" section. We will assume you create an Open Section first, in
the site root. It will be Private by default, otherwise make it so. Note that
the title and description will be exposed, to provide potential subscribers
some information about what they're signing up for.

    Change its title to "My Open Section" afterwards, or update the catalog
    because of issue #1.

After marking the Folder as a Subscribable Section in this manner, an extra tab
"Subscriptions" appears (next to "Sharing"). Here you can view subscriptions
and subscription requests for the Subscribable Section. 

Also, you should see a portlet in the right column which shows your recently
created "Open Section". The portlet was added when the product was installed,
and only shows when there are Subscribable Sections. 

Subscribing to an Open Section
------------------------------

A Member without any further privileges won't see the Open Section in the
site's sections menu, but will see it in the portlet. Clicking it takes you to
it. You'll be redirected to the Plone's `insufficient_privileges` form, which
is patched to not display the "Insufficient Privileges" message, but which
instead tells you that this is a Section for which a subscription is required,
and there'll be a link to subscribe to the Section. The title and description
of the Section will be visible, so you know what the Section is about..

Clicking the subscription link on the Open Section will immediately grant you
the Reader role on the Section. You'll be redirected to the default view of the
Section, and a portal message will tell you your subscription was succesful.

Viewing and removing subscriptions
----------------------------------

As the Manager, you will now see this member's subscription in the
"Subscriptions" overview. You will also find the user has the "Reader" role
under the Sharing tab. 
    
    If there are members in the Sharing list that are not in the Subscribers
    list, it means that they have not been added via this product. You can only
    manage these members through Plone's Sharing form (and not via our "Manage
    subscriptions" screen), because these members are not subscribers.

    If you revoke a subscriber's Reader role from the Sharing tab, the
    subscriber will also not show up as a subscriber in the "Manage
    subscriptions" screen anymore. 

In this form, you can check the box to remove the subscription. Submit the
form, and you'll see the subscription has disappeared.  If you look under
"Sharing", you'll notice the Reader role has also been removed.

Subscribing to a Closed Section
-------------------------------

This is similar to subscribing to an Open Section, but after subscribing you'll
see a list of your subscriptions. The top of the screen shows a message which
says that your subscription request has been added.

As a manager, you will see this request in the "Subscription requests" portlet
which was also added to the right column upon product installation. Clicking
the link will take you to the Section's "Manage subscriptions" page.

Approving subscriptions
-----------------------

On the subscriptions management form of the Closed Section, the Manager will
see a list of subscription requests. Checking the box in the "Approve" column
and submitting the form will approve the request: You'll see a portal message
saying the subscription was approved. You'll see the user has been moved from
the "Requests" to the "Subscriptions" list. Looking at the "Sharing", you'll
notice the user has been granted the Reader role.

Issues
======

A list of issues per User Story:

1. (User Story #2) p4a.subtyper doesn't re-index the object after it alters its
   interfaces, so the list of Subscribable Section Folders in the portlet isn't
   updated until someone changes the folders or updates the catalog.

Authors
=======

Kees Hink
