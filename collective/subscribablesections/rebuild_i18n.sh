#!/bin/sh
I18NDUDE="../../../../bin/i18ndude"
I18NDOMAIN="collective.subscribablesections"

# Synchronise the templates and scripts with the .pot.
# All on one line normally:
$I18NDUDE rebuild-pot --pot locales/${I18NDOMAIN}.pot \
    --merge locales/manual.pot \
    --create ${I18NDOMAIN} \
    ./ \
    ./profiles/default

# Synchronise the resulting .pot with all .po files
for po in locales/*/LC_MESSAGES/${I18NDOMAIN}.po; do
    $I18NDUDE sync --pot locales/${I18NDOMAIN}.pot $po
done

# Synchronise the templates and scripts with the .pot.
i18ndude rebuild-pot --pot ./locales/plone.pot \
    --create plone \
    ./configure.zcml \
    ./profiles/default

# Synchronise the Plone's pot file (Used for the workflows)
for po in ./locales/*/LC_MESSAGES/plone.po; do
    i18ndude sync --pot ./locales/plone.pot $po
done
