from pyannote.core import Annotation, Timeline, Segment
from pyannote.metrics.segmentation import SegmentationPrecision, SegmentationRecall, SegmentationCoverage, SegmentationPurity



precision_score = SegmentationPrecision(tolerance=0.5)
recall_score = SegmentationRecall(tolerance=0.5)
coverage_score = SegmentationCoverage(tolerance=0.5)
purity_score = SegmentationPurity(tolerance=0.5)

reference = Timeline()
reference_annotation = Annotation()
reference.add(Segment(0, 1))
reference.add(Segment(1, 2))  # Could not skip this part even if it is silence part; skip this part would affect coverage score
reference.add(Segment(2, 4))
reference_annotation[Segment(0, 1)] ='speaker1'
reference_annotation[Segment(1, 4)] ='speaker2'


hypothesis = Timeline()
hypothesis.add(Segment(0, 4))
print(precision_score(reference, hypothesis))
print(recall_score(reference,hypothesis))
print(coverage_score(reference_annotation, hypothesis))
print(purity_score(reference_annotation,hypothesis))

hypothesis = Timeline()
hypothesis.add(Segment(0, 3))
hypothesis.add(Segment(3, 4))

print(precision_score(reference, hypothesis))
print(recall_score(reference,hypothesis))

reference = Timeline()
reference_annotation = Annotation()
reference.add(Segment(0, 1))
# reference.add(Segment(1, 2))  # Could not skip this part even if it is silence part; skip this part would affect coverage score
reference.add(Segment(2, 4))
reference_annotation[Segment(0, 1)] ='speaker1'
reference_annotation[Segment(2, 4)] ='speaker2'


hypothesis = Timeline()
hypothesis.add(Segment(0, 4))
print(precision_score(reference, hypothesis))
print(recall_score(reference,hypothesis))
print(coverage_score(reference_annotation, hypothesis)) #Coverage score should be 0.75 instead of 1, not accurate by skipping the second part
print(purity_score(reference_annotation,hypothesis))


