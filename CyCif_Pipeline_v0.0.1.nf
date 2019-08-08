// Input

myDir = file("/n/groups/lsp/cycif/example_data/")
myDir.eachFile { item ->
    if( item.isFile() ) {
        println "${item.getName()} - size: ${item.size()}"
    }
    else if( item.isDirectory() ) {
        println "${item.getName()} - DIR"
    }
}








// sticher

// prob map

// segmenter

// feature extractor

/*
process sticher {
	publishDir '/n/groups/lsp/cycif/example_data/image_1/registration'	
	
	queue 'short'
	time '2h'
	memory '64 GB'

	conda '/n/groups/lsp/cycif/ashlar'

	input:
	file('/n/groups/lsp/cycif/cycif_pipeline_testing_space/ashlar_dirs.csv')

	output:
	//file('*.tif') into sticher_output_channel mode flatten
	file('image_1.ome.tif') into sticher_output_channel

	script:	
	'''
	python /n/groups/lsp/cycif/ashlar/lib/run_ashlar_csv_batch_v1.7.0.py /n/groups/lsp/cycif/cycif_pipeline_testing_space/ashlar_dirs.csv
	'''
}
*/
