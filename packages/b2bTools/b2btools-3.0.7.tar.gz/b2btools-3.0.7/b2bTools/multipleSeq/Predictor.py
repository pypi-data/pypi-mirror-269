import numpy as np

from b2bTools.singleSeq.Predictor import MineSuite
from b2bTools.general.Io import B2bIo


class MineSuiteMSA(MineSuite):

    scriptName = "b2bTools.msaBased.Predictor"

    def predictSeqsFromMSA(self, msaFile, gapCode='-', predTypes=[]):
        # This will read in alignment, should automatically detect format. Code is in general/Io.py
        self.seqAlignments = self.readAlignments(msaFile, resetAlignRefSeqID=True, gapCode=gapCode)

        seqs = [(seqId, self.seqAlignments[seqId].replace(gapCode, '')) for seqId in self.seqAlignments.keys()]

        self.predictSeqs(seqs, predTypes=[*predTypes])

        # Now self.allPredictions will give you the predictions for all the individual sequences in the MSA!

    def predictAndMapSeqsFromMSA(self, msaFile, gapCode='-', dataRead=False, predTypes=[]):
        # Read in data only if not yet present - can re-use this function within instance of class if data already present!
        if not dataRead:
            self.predictSeqsFromMSA(msaFile, gapCode=gapCode, predTypes=[*predTypes])

        self.allSeqIds = list(self.seqAlignments.keys())
        self.allSeqIds.sort()

        # All the current prediction types
        prediction_keynames = list(self.allPredictions[self.allSeqIds[0]].keys())
        execution_times = []
        single_values = []

        if 'dynamine_execution_time' in prediction_keynames:
            prediction_keynames.remove('dynamine_execution_time')
            execution_times.append('dynamine_execution_time')

        if 'disomine_execution_time' in prediction_keynames:
            prediction_keynames.remove('disomine_execution_time')
            execution_times.append('disomine_execution_time')

        if 'efoldmine_execution_time' in prediction_keynames:
            prediction_keynames.remove('efoldmine_execution_time')
            execution_times.append('efoldmine_execution_time')

        if 'agmata_execution_time' in prediction_keynames:
            prediction_keynames.remove('agmata_execution_time')
            execution_times.append('agmata_execution_time')

        if 'psper_execution_time' in prediction_keynames:
            prediction_keynames.remove('psper_execution_time')
            execution_times.append('psper_execution_time')

        if 'protein_score' in prediction_keynames:
            prediction_keynames.remove('protein_score')
            single_values.append('protein_score')

        # self.predictionTypes = predictionTypes
        self.prediction_keynames = prediction_keynames
        self.allAlignedPredictions = {}
        sequenceInfo = {}

        for seq_id in self.allSeqIds:
            alignment = self.seqAlignments[seq_id]

            sequenceInfo[seq_id] = []
            self.allAlignedPredictions[seq_id] = {}

            for predictionType in prediction_keynames:
                if predictionType in single_values or predictionType in execution_times:
                    self.allAlignedPredictions[seq_id][predictionType] = None
                else:
                    self.allAlignedPredictions[seq_id][predictionType] = []

            sequenceResidueIndex = 0
            for alignResidue in [r for r in alignment]:
                sequenceInfo[seq_id].append(alignResidue)

                if alignResidue == self.gapCode:
                    for predictionType in prediction_keynames:
                        if (not predictionType in single_values) and (not predictionType in execution_times):
                            self.allAlignedPredictions[seq_id][predictionType].append(None)
                else:
                    for predictionType in prediction_keynames:
                        if (not predictionType in single_values) and (not predictionType in execution_times):
                            try:
                                current_value_tuple = self.allPredictions[seq_id][predictionType][sequenceResidueIndex]
                                current_residue, current_prediction_value, *_other_values = current_value_tuple

                                assert current_residue == alignResidue or current_residue == 'X', f"Amino acid code mismatch {current_residue}-{alignResidue}"

                                self.allAlignedPredictions[seq_id][predictionType].append(current_prediction_value)
                            except ValueError:
                                raise ValueError(
                                    f"Predicted value of type '{predictionType}' not found for input sequence '{seq_id}'")

                    sequenceResidueIndex += 1

            for single_value in [*single_values, *execution_times]:
                valueFloat = self.allPredictions[seq_id][single_value]
                self.allAlignedPredictions[seq_id][single_value] = valueFloat

        self.allAlignedPredictions['sequence'] = sequenceInfo

    def filterByRefSeq(self, refSeqId):

        assert refSeqId in self.allSeqIds,  'Reference sequence ID {} missing in current prediction information!'.format(
            refSeqId)

        # Here filter so that get back values in reference to the sequence ID that is given.

    def getDistributions(self):

        distribKeys = ('median', 'thirdQuartile', 'firstQuartile', 'topOutlier', 'bottomOutlier')
        numDistribKeys = len(distribKeys)

        # Now generate the info for quartiles, ... based on the alignRefSeqID, first entry in alignment file
        self.alignedPredictionDistribs = {}

        for predictionType in self.prediction_keynames:
            self.alignedPredictionDistribs[predictionType] = {}
            for distribKey in distribKeys:
                self.alignedPredictionDistribs[predictionType][distribKey] = []

        # Loop over whole alignment
        alignmentLength = len(self.seqAlignments[self.allSeqIds[0]])

        for alignIndex in range(alignmentLength):
            for predictionType in self.prediction_keynames:
                predValues = [self.allAlignedPredictions[seqId][predictionType][alignIndex] for seqId in self.allSeqIds if
                              self.allAlignedPredictions[seqId][predictionType][alignIndex] != None]

                distribInfo = self.getDistribInfo(predValues)

                for i in range(numDistribKeys):
                    self.alignedPredictionDistribs[predictionType][distribKeys[i]].append(distribInfo[i])

        self.jsonData = B2bIo.getAllPredictionsJson_msa(self, results=self.alignedPredictionDistribs)
        return self.jsonData

    def getDistribInfo(self, valueList, outlierConstant=1.5):
        # JR: I put this try-except cause in some MSA we may have only one sequence
        # so the distribution values cannot be calculated
        try:
            median = np.median(valueList)
            upper_quartile = np.percentile(valueList, 75)
            lower_quartile = np.percentile(valueList, 25)
            IQR = (upper_quartile - lower_quartile) * outlierConstant

            return (median, upper_quartile, lower_quartile, upper_quartile + IQR, lower_quartile - IQR)

        except:
            return (None, None, None, None, None)
