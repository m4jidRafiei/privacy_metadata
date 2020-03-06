from p_privacy_metadata.privacyExtension import privacyExtension
from p_privacy_metadata.PMA import PMA
from pm4py.objects.log.importer.xes import factory as xes_importer_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
import pandas as pd

event_log = "Paper sample.xes"
log = xes_importer_factory.apply(event_log)

# privacyExtension Part----------------------------------------------------------------
prefix = 'privacy:'
uri = 'http://www.xes-standard.org/privacy.xesext'
privacy = privacyExtension(log, prefix, uri)
privacy.set_privacy_tracking(operation='suppression', level='event', target='org:resource')

statistics={}
statistics['no_modified_traces'] = 15
statistics['no_modified_events'] = 20
desired_analyses= {}
desired_analyses['1']='process discovery'
desired_analyses['2']='social network discovery'
message = privacy.set_optional_tracking(layer = 1, statistics=statistics, desired_analyses=desired_analyses, test='test' )
print(message)

layer = privacy.get_layer(layer=1)
anon = privacy.get_anonymizations()

xes_exporter.export_log(log, 'ext_paper_sample.xes')

# PMA Part----------------------------------------------------------------------------
try:
    log_name = log.attributes['concept:name']
except Exception as e:
    log_name = "No mame is given for the event log!"

pma = PMA()
pma_desired_analyses = ['analysis 1', 'analysis 2']
data = {'Name': ['Tom', 'nick', 'krish', 'jack'], 'Age': [20, 21, 19, 18]}
df = pd.DataFrame(data)
pma.set_values(origin=log_name, method='method 1', desired_analyses=pma_desired_analyses,data=df.copy())
pma.create_xml('pma_paper_sample.xml')
print(pma.get_values()['data'])
pma = pma.read_xml("pma_paper_sample.xml")
print(pma)





