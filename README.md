## Introduction
This project implements the privacy metadata proposed in the paper [Privacy-Preserving Data Publishing in Process Mining](https://).
## Python package
The implementation has been published as a standard Python package. Use the following command to install the corresponding Python package:

```shell
pip install p-privacy-metadata
```

## Usage
```python
from p_privacy_metadata.privacyExtension import privacyExtension
from p_privacy_metadata.ELA import ELA
from pm4py.objects.log.importer.xes import factory as xes_importer_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
import pandas as pd

event_log = "paper_sample.xes"
log = xes_importer_factory.apply(event_log)

# privacyExtension Part
prefix = 'privacy:'
uri = 'paper_version_uri/privacy.xesext'
privacy = privacyExtension(log, prefix, uri)
privacy.set_anonymizer(operation='suppression', level='event', target='org:resource')

statistics={}
statistics['no_modified_traces'] = 15
statistics['no_modified_events'] = 20
desired_analyses= {}
desired_analyses['1']='process discovery'
desired_analyses['2']='social network discovery'
message = privacy.set_optional_anonymizer(layer = 1, statistics=statistics, desired_analyses=desired_analyses, test='test' )
print(message)

layer = privacy.get_anonymizer(layer=1)
anon = privacy.get_anonymizations()

xes_exporter.export_log(log, 'ext_paper_sample.xes')

# ELA Part
try:
    log_name = log.attributes['concept:name']
except Exception as e:
    log_name = "No mame is given for the event log!"

ela = ELA()
ela_desired_analyses = ['analysis 1', 'analysis 2']
data = {'Name': ['Tom', 'nick', 'krish', 'jack'], 'Age': [20, 21, 19, 18]}
df = pd.DataFrame(data)
ela.set_values(origin=log_name, method='method 1', desired_analyses=ela_desired_analyses,data=df.copy())
ela.create_xml('ela_paper_sample.xml')
print(ela.get_values()['data'])
ela = ela.read_xml("ela_paper_sample.xml")
print(ela)
```
