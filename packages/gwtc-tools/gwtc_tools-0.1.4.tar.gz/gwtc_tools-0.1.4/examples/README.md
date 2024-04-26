# Example of how to use this library

Below is a tutorial for how to use the gwtc-tools library. The service URLS point to gracedb-test, so it is appropriate to follow these instructions end to end even though they will modify the global test version of GWTC-4. **DO NOT FOLLOW THESE EXACT INSTRUCTIONS USING PRODUCTION GRACEDB.**

NOTE you might want to make a test directory to run these commands in.

## Authorized users

For many operations, only users authorized to upload events for a given pipeline will be able to run some of these instructions.  **If you are, e.g., a pycbc authorized user, modify some of the examples below to upload pycbc events, etc.**  Contact Chad Hanna (chad.hanna@ligo.org) and Alex Pace (alexander.pace@ligo.org) for authorization questions.

## Installation

This code will soon be available in the igwn conda distribution. For now, it is pip installable.  

<details>

<summary>Many clusters have a suitable IGWN distribution enabled by default, if not click here for an example to setting up an IWGN environment</summary>

```
source /cvmfs/oasis.opensciencegrid.org/ligo/sw/conda/etc/profile.d/conda.sh && conda activate igwn-py39 && export PATH=${PATH}:~/.local/bin
```

</details>

Once you have a suitable igwn environment, you can install with

```
pip install --user gwtc-tools
```

Or, if you wish, install from source in this repo.

## Resetting the catalog for a given pipeline

**NOTE: it is fine to do this on gracedb test for the purposes of this tutorial, but you should be careful doing the below on production. Only do this if you are positive that you want to delete and replace all events in the catalog for a given pipeline.**

First I reset all of the gwtc information in gracedb test (this has to be done pipeline by pipeline)
```
$ gwtc_update_pipeline_gevents --reset --pipeline gstlal --group CBC --search AllSky --service-url https://gracedb-test.ligo.org/api/ --number 4
$ gwtc_update_pipeline_gevents --reset --pipeline spiir --group CBC --search AllSky --service-url https://gracedb-test.ligo.org/api/ --number 4
$ gwtc_update_pipeline_gevents --reset --pipeline MBTA --group CBC --search AllSky --service-url https://gracedb-test.ligo.org/api/ --number 4
$ gwtc_update_pipeline_gevents --reset --pipeline pycbc --group CBC --search AllSky --service-url https://gracedb-test.ligo.org/api/ --number 4
```

## Uploading new events

Before the next steps, copy the contents of the examples directory to your current directory.

Upload events (Try modifying the yaml file and pipeline etc for your use case.)

```
$ gwtc_update_pipeline_gevents --pipeline gstlal --group CBC --search AllSky --number 4 --in-yaml gstlalv1.yaml --out-yaml gstlal_processedv1.yaml
INFO:root:Uploaded G651753
INFO:root:Uploaded G651754
INFO:root:associated super event S230522a with gevent G651754
INFO:root:associated super event S230824d with gevent G651753
INFO:root:Uploading
{
    "S230522a": {
        "pipelines": {
            "gstlal": "G651754"
        },
        "far": 3.171756306943489e-16,
        "pastro": null
    },
    "S230824d": {
        "pipelines": {
            "gstlal": "G651753"
        },
        "far": 1.611950746698324e-13,
        "pastro": null
    }
}
INFO:root:Created GWTC:
{
    "number": "4",
    "version": 53,
    "created": "2024-02-28 14:52:25 UTC",
    "submitter": "chad.hanna@ligo.org",
    "gwtc_superevents": {
        "S230824d": {
            "pipelines": {
                "gstlal": "G651753"
            },
            "far": 1.611950746698324e-13,
            "pastro": null
        },
        "S230522a": {
            "pipelines": {
                "gstlal": "G651754"
            },
            "far": 3.171756306943489e-16,
            "pastro": null
        }
    },
    "comment": ""
}
```

You can see that the GIDs were added to the output yaml file. This is just meant as a convenience for the user at this point, but we may  build tools that will rely on this for updates in the future.

```
$ cat gstlal_processedv1.yaml 
- coinc: H1L1-GSTLAL_AllSky-1376883065-0.xml.gz
  gid: G651753
  pastro: null
- coinc: L1-GSTLAL_AllSky-1368783503-0.xml.gz
  gid: G651754
  pastro: null
```

## Checking the differences between catalog revisions

Check the diff

```
$ gwtc_diff
INFO:root:Calculating catalog diff from versions None to None
INFO:root:
- new s events in version 53: ['S230522a', 'S230824d']
- deleted s events in version 53: []
- changed s events in version 53:
```

## Upload a new version of some events.

```
$ gwtc_update_pipeline_gevents --pipeline gstlal --group CBC --search AllSky --number 4 --in-yaml gstlalv2.yaml --out-yaml gstlal_processedv2.yaml
```

Check the diff

```
$ gwtc_diff
INFO:root:Calculating catalog diff from versions None to None
INFO:root:
- new s events in version 54: ['S230513ar']
- deleted s events in version 54: []
- changed s events in version 54:

	S230824d:
		pipelines: {'gstlal': 'G651753'} -> {'gstlal': 'G651772'}

	S230522a:
		pastro: None -> {'BBH': 1.0, 'BNS': 0.0, 'NSBH': 0.0, 'Terrestrial': 0.0}
		pipelines: {'gstlal': 'G651754'} -> {'gstlal': 'G651773'}
```

## Retrieve g event files

```
(igwn) [chad.hanna@ldas-pcdev1 git]$ gwtc_get_gevent_coinc_files --pipeline gstlal --proxy-path /tmp/x509up_u40120 --version <version>
```