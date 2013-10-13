This folder contains the script to use the current training data to train an R model and upload to yhat.
Follow the following instructions:

[1] Output all the training data to a file named "dat.tsv" to this folder. You should overwrite the existing file. The suffix "tsv" means "tabulator seprated values".

[2] The format of "dat.tsv" should be one record per row, tab separated, no header.

[3] Each row of "dat.tsv" should contain 13 rows. They are
    Userid
    Visa Type
    Visa Entry ("New" or "Renewal")
    City
    Major
    Status ("Clear")
    Begin Year
    Begin Month
    Begin Date
    End Year
    End Month
    End Date
    Wait time

[4] A sample is here:
lc	B1	New	ShangHai	Computer Science/Engineering	Clear	2008	11	12	2009	4	14	153
tjaliang	H4	New	BeiJing	Physics	Clear	2008	11	24	2009	3	12	108
dolong	H4	New	Others	Chemistry	Clear	2008	12	1	2009	3	17	106
Kevin	J1	Renewal	BeiJing	Biochemical Engineering	Clear	2008	12	1	2009	3	17	106
jzl	H1	Renewal	BeiJing	Materials Science/Engineering	Clear	2008	12	2	2009	3	19	107
heartlake	H1	Renewal	BeiJing	Neuroscience	Clear	2008	12	2	2009	3	17	105

[5] If any field is missing in out dataset, do not leave it blank, just generate a place_holder, such as 0 for numbers, or NA for strings.

[6] After preparing "dat.tsv", cd into the "model-pipeline" folder, and run the script "update-model.sh". You should put something like this in your script:

cd /root/checkoo/util/regression/model-pipeline
./update-model.sh

[7] If you manually run this, you will see that the program print out the version number at the end.
The name of the model is: "Checkoo R Linear Regression"
Or you can run the script "./check-version.R" to print out versions, so that you can know which is the latest version.

[8] If you update our model everyday, then you should increment the version number automatically.
