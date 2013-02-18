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

WARNINGS=`find . -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-WARN' | wc -l`
ERRORS=`find . -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-ERROR' | wc -l`
FATAL=`find . -name "*pt"  | xargs i18ndude find-untranslated | grep -e '^-FATAL' | wc -l`

echo
echo "There are $WARNINGS warnings \(possibly missing i18n markup\)"
echo "There are $ERRORS errors \(almost definitely missing i18n markup\)"
echo "There are $FATAL fatal errors \(template could not be parsed, eg. if it\'s not html\)"
echo "For more details, run \'find . -name \"\*pt\" \| xargs i18ndude find-untranslated\' or"
echo "Look the rebuild i18n log generate for this script called \'rebuild_i18n.log\' on locales dir"

rm ./rebuild_i18n.log

touch ./rebuild_i18n.log

find ../ -name "*pt" | xargs i18ndude find-untranslated > rebuild_i18n.log
