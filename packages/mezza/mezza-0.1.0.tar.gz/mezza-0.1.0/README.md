# MezzeCMS

Mezze is a ready-to-go, open-source, headless CMS written in Python and Django.

Unlike many other Python/Django CMSes, Mezze doesn't require any coding to get started, but you can drop in to Django if you need to customise things.

## Installation

```sh
pip install mezzecms
mezze migrate
mezze createsuperuser
mezze runserver
```

This will create an SQLite database in the local folder, create a user and boot up Mezze on [localhost port 8000](http://localhost:8000).

### Using PostgreSQL

You can pass in the URL to a PostgreSQL database using a ``DATABASE_URL`` environment variable:

```sh
export DATABASE_URL=postgresql://localhost/mezzedb
mezze migrate
mezze createsuperuser
mezze runserver
```

## Design of Mezze

### Built-in types

Mezze comes with a selection of pre-built content types that are built in to the base system and cannot be changed.
You can either use these types directly or create custom types based on them that are extended with custom fields.
All of these types are optional and can be disabled if not required.

 - **Content** - The base type for all content, this includes some metadata such as the title, locale, status, and more
   - **Page** - The base type for all web content. This adds a 'path' field giving the content a URL.
     - **Post** - Represents point-in-time content such as blog posts, news articles, video pages, etc.
     - **Event** - Represents event information and adds calendar export functionality
     - **Person** - Represents a person
     - **Product** - Represents a product for sale
   - **Asset** - The base type for embeddable content, these are displayed in the "Assets" section of the UI
     - **FileAsset** - The base type for all media types that are uploaded to the CMS
       - **Image** - Represents images uploaded to the CMS, includes extra fields for image size. Provides functions for resizing and cropping the images
       - **Document** - Represents multi-page document files such as PDFs
     - **MuxVideo** - Represents a video uploaded to Mux.io
     - **SocialMediaPost** - Represents any post uploaded to a social media platform

*Design note: We decided to provide these types out of the box so that we can provide a standard base for extensions to integrate with. For example, a Shopify extension would be able to know exactly what the base fields of Product are.*

