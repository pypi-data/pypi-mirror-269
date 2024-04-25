# -*- coding: utf-8 -*-
from b2bTools.singleSeq.PSPer.phase_transition_hmm import phase_hmm
import string
import time
import numpy as np


def read_fasta(database):
	with open(database, 'r') as f:
		uniprot_lines = f.readlines()

	sequences_dict = {}

	for line in uniprot_lines:
		if line[0] == '>':
				uniprotid = line.strip('>\n')
				sequences_dict[uniprotid] = ''
		else:
			sequences_dict[uniprotid] = sequences_dict[uniprotid] + line.strip('\n').upper()

	return sequences_dict

def standalone(input_obj):
	times = {}

	def check_sequences(seqs):
		for sequence_key in list(seqs.keys()):

			tic = time.perf_counter()

			if sequence_key == 'extra_predictions':
				toc = time.perf_counter()
				times[sequence_key] = (toc - tic)
				continue

			elif not seqs[sequence_key].isalpha():
				toc = time.perf_counter()
				times[sequence_key] = (toc - tic)

				return {'error':'invalid char in sequence '+sequence_key}

			elif len(seqs[sequence_key]) > 3000:
				toc = time.perf_counter()
				times[sequence_key] = (toc - tic)

				return {'error':'sequence '+sequence_key+' too long, maximum length is 3000 amino acids'}

			elif len(seqs[sequence_key]) < 20:
				toc = time.perf_counter()
				times[sequence_key] = (toc - tic)

				return {'error':'sequence '+sequence_key+' short, minimum length is 20 amino acids'}
			else:
				toc = time.perf_counter()
				times[sequence_key] = toc - tic

		return True

	def load_model():
		mod = phase_hmm()
		mod.fit()

		scaler = None

		return mod, scaler

	def format_output(disorder, viterbi, seqs, features):
		protein_id_keys = list(disorder.keys())

		formatted_output_list = []

		for protein_id_index in range(len(protein_id_keys)):
			tic = time.perf_counter()

			protein_id = protein_id_keys[protein_id_index]
			current_features = features[protein_id]

			for feature_index in range(5):
				actual = current_features[:, feature_index]
				base   = current_features[:, 0]

				assert len(actual) == len(base)

			features[protein_id] = np.array(current_features)

			entry = {}
			entry['proteinID'] = protein_id
			entry['sequence'] = seqs[protein_id]
			entry['protein_score']=disorder[protein_id]
			entry['viterbi'] = viterbi[protein_id] if protein_id in viterbi else np.full(len(seqs[protein_id]), '')
			entry['complexity'] = list(features[protein_id][:,0])
			entry['arg'] = list(features[protein_id][:,1])
			entry['tyr'] = list(features[protein_id][:,2])
			entry['RRM'] = list(features[protein_id][:,3])
			entry['disorder'] = list(features[protein_id][:,4])

			toc = time.perf_counter()
			entry['psper_execution_time'] = times[protein_id] + (toc - tic)

			formatted_output_list.append(entry)

		return { 'results': formatted_output_list }

	def predict_fasta(sequence_input, model, model_load_time, crunch=100):
		if type(sequence_input) == str:
			try:
				fasta_sequences=read_fasta(sequence_input)
			except:
				return {'error': "Problems in the FASTA file: input is not string"}
		elif type(sequence_input) == dict:
			fasta_sequences = sequence_input
		else:
			return {'error': 'Internal error, wrong object passed to the standalone, it must be either a dict or a string'}

		check = check_sequences(fasta_sequences)
		if check is not True:
			return check

		model_building_time_tic = time.perf_counter()

		built_vector = model.build_vector(fasta_sequences)
		results_dict = model.predict_proba(built_vector)
		viterbi = model.viterbi(built_vector)

		model_building_time_toc = time.perf_counter()

		model_building_time = model_building_time_toc - model_building_time_tic

		dict_features = {}

		printable_characters = [*string.printable]

		for sequence_key in built_vector.keys():
			tic = time.perf_counter()

			seq_vector = []

			for seq_vector_element in built_vector[sequence_key]:
				temp_seq_vector = []

				for element_feature in seq_vector_element:
					feature_char_index = printable_characters.index(element_feature)
					temp_seq_vector += [float(feature_char_index)]

				seq_vector += [temp_seq_vector]

			toc = time.perf_counter()
			psper_execution_time = toc - tic

			times[sequence_key] = times[sequence_key] + model_load_time + model_building_time + psper_execution_time

			dict_features[sequence_key] = np.array(seq_vector)

		results = format_output(results_dict, viterbi, fasta_sequences, dict_features)
		return results

	# This should not be necessary with new disomine setup, commented out
	#clean_psipred_tmp()
	model_load_time_tic = time.perf_counter()
	phase_hmm_instance, _ = load_model()
	model_load_time_toc = time.perf_counter()

	model_load_time = model_load_time_toc - model_load_time_tic

	results = predict_fasta(input_obj, phase_hmm_instance, model_load_time)

	return results

def main(args):
	#print standalone("example.fasta")
	fasta_sequences=read_fasta('input_files_examples/example_toy.fasta')
	fasta_sequences['extra_predictions']=False
	print(standalone(fasta_sequences))
	#from memory_profiler import memory_usage
	#mem_usage = memory_usage(standalone,interval=0.01)
	#print('Memory usage (in chunks of .1 seconds): %s' % mem_usage)
	#print('Maximum memory usage: %s' % max(mem_usage))
	#cProfile.run('standalone("example.fasta")')

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
