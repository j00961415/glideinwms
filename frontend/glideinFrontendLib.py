#
# Description:
#   This module implements the functions needed to keep the
#   required number of idle glideins
#
# Author:
#   Igor Sfiligoi (Sept 19th 2006)
#

import condorMonitor,condorExe

#
# Return a dictionary of schedds containing interesting jobs
# Each element is a condorQ
#
# If not all the jobs of the schedd has to be considered,
# specify the appropriate constraint
#
def getCondorQ(schedd_names,constraint=None):
    return getCondorQConstrained(schedd_names,"(JobStatus=?=1)||(JobStatus=?=2)",constraint)

#
# Return a dictionary of schedds containing idle jobs
# Each element is a condorQ
#
# Use the output of getCondorQ
#
def getIdleCondorQ(condorq_dict):
    out={}
    for schedd_name in condorq_dict.keys():
        sq=condorMonitor.SubQuery(condorq_dict[schedd_name],lambda el:el['JobStatus']==1)
        sq.load()
        out[schedd_name]=sq
    return out

#
# Return a dictionary of schedds containing idle jobs
# Each element is a condorQ
#
# Use the output of getCondorQ
#
def getRunningCondorQ(condorq_dict):
    out={}
    for schedd_name in condorq_dict.keys():
        sq=condorMonitor.SubQuery(condorq_dict[schedd_name],lambda el:el['JobStatus']==2)
        sq.load()
        out[schedd_name]=sq
    return out

#
# Get the number of jobs that match each glidein
#
# match_str = '(job["MIN_NAME"]<glidein["MIN_NAME"]) && (job["ARCH"]==glidein["ARCH"])'
# condorq_dict = output of getidlqCondorQ
# glidein_dict = output of interface.findGlideins
#
# Returns:
#  dictionary of glidein name
#   where elements are number of idle jobs matching
def countMatch(match_str,condorq_dict,glidein_dict):
    match_obj=compile(match_str,"<string>","eval")
    out_glidein_counts={}
    for glidename in glidein_dict:
        glidein=glidein_dict[glidename]
        glidein_count=0
        for schedd in condorq_dict.keys():
            condorq=condorq_dict[schedd]
            condorq_data=condorq.fetchStored()
            schedd_count=0
            for jid in condorq_data.keys():
                job=condorq_data[jid]
                if eval(match_obj):
                    schedd_count+=1
                pass
            glidein_count+=schedd_count
            pass
        out_glidein_counts[glidename]=glidein_count
        pass
    return out_glidein_counts


############################################################
#
# I N T E R N A L - Do not use
#
############################################################

#
# Return a dictionary of schedds containing jobs of a certain type 
# Each element is a condorQ
#
# If not all the jobs of the schedd has to be considered,
# specify the appropriate additional constraint
#
def getCondorQConstrained(schedd_names,type_constraint,constraint=None):
    out_condorq_dict={}
    for schedd in schedd_names:
        condorq=condorMonitor.CondorQ(schedd)
        full_constraint=type_constraint[0:] #make copy
        if constraint!=None:
            full_constraint="(%s) && (%s)"%(full_constraint,constraint)

        try:
            condorq.load(full_constraint)
        except condorExe.ExeError:
            continue # if schedd not found it is equivalent to no jobs in the queue
        if len(condorq.fetchStored())>0:
            out_condorq_dict[schedd]=condorq
    return out_condorq_dict

