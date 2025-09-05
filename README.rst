============================================================
Ready
============================================================

Ready is a Django app for tracking inventory of emergency supplies.
Track costs, quantities, and expiration dates of food, first-aid kits, and other supplies.


Work in progress: To-do list
------------------------------------------------------------

Item hierarchy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Situation:** Item instances are categorized in the following hierarchy: Category > Groups > Items.
For example, a specific brand of granola bar might be categorized as: Food > Snacks > Granola.
A specific package of bandages might be categorized as: First Aid > General > Bandages.

**Problem:** "Categories," "groups," and "items" can only be added through the admin site.

**TO-DO:** Make it possible for users to add "groups" and "items" through the main site (cf. "Categories," below).

Categories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Situation:** Icons in the base template sidebar are links to forms to add three categories of supplies: food, first aid, and general.
The links are hard coded into the application templates.

**Problem:** "Categories" can only be added through the admin site.
For these buttons to work, an admin must first add "Food," "First Aid," and "Supplies" as categories in the admin site.

**TO-DO:** Hard code these categories into the application to make the buttons work as soon as the application is included in a site.

Locations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Situation:** Item instances can be stored in different locations set up in the admin site (cf. "Item hierarchy," above). Example locations: a backpack, a basement, an office, etc.

**Problem:** There is no way for users to relocate items from one location to another.

**TO-DO:** Add a button to relocate items (similar to the "consume" and "store" buttons found in the "detail" sections on the home page).


Installation
------------------------------------------------------------

Clone this repository, change into the directory, and install the application with ``pip``:

.. code-block:: console

  $ git clone https://github.com/elijahgreenstein/ready.git
  $ cd ready
  $ pip install .


Quick start
------------------------------------------------------------

#. Set up a new app with Django. For example:

    .. code-block:: console

      $ django-admin startproject supplies

#. Change into the new directory with ``cd supplies``.
#. Add ``ready`` to the ``INSTALLED_APPS`` settings in ``supplies/settings.py``::

   INSTALLED_APPS = [
       ...,
       "ready",
   ]

#. Include the ready URLconf in your project ``urls.py``::

   path("ready/", include("ready.urls")),

#. Run ``python manage.py migrate`` to create the models.


Set up
------------------------------------------------------------

The Ready app is used to add, relocate, and remove supplies from different locations (e.g. a stock of supplies in a home or office).

Before users can track supplies, an admin must first create categories of items, storage locations, units, etc. through the Django admin page.

#. Set up an `admin user <https://docs.djangoproject.com/en/5.2/intro/tutorial01/>`_:

    .. code-block:: console

      $ python manage.py createsuperuser

#. Start the development server:

    .. code-block:: console

      $ python manage.py runserver

#. Open a web browser and navigate to the admin page, e.g. http://127.0.0.1:8000/admin/.
#. Log in with the superuser account. 
#. Add options to the following: "Category," "Groups," "Items," "Stores," and "Units."

Once an admin user has configured the application, users can visit the ``/ready/`` URL (e.g. http://127.0.0.1:8000/ready/) to add and remove inventory.


Usage
------------------------------------------------------------

* Use the icons below the Ready "R" icon to add food, first aid, or general inventory.
* View the inventory in specific locations by selecting locations from the sidebar.
* On the home page, select "summary" for information about stocks of different kinds of supplies.
* On the home page, select "details" for a list of specific packages of food, first aid supplies, or general supplies. Use the "C" or "S" buttons to consume or move goods into long-term storage, respectively.
* Warnings will appear under "Alerts" on the home page when inventory falls below target stocks, or when specific goods are nearing or have passed expiration dates.

