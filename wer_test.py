from libs.wer import wer
from libs.wer import clean_extra_words

ref = "Yeah, I could tell, since you didn't call or write the entire time it was happening. No, I know, I was just"
hyp1 = "(music in background) A: Yeah, I could tell, since you didn't call her right as it was happening B: No, I was just"
hyp2 = "Yeah, I could tell, since you didn't call her right as it was happening No, I was just"

wer1 = wer(ref, hyp1)
wer2 = wer(ref, hyp2)
# print(wer1, ';', wer2)

print(clean_extra_words(ref, hyp1))

ref = "the dedicated detectives who investigate these vicious felonies are members of an elite squad known as the special victims unit."
hyp1 = "Opening of Law and Order: SVU -- The dedicated detectives who investigate these vicious crimes are known as the Special Victims Unit"
hyp2 = "The dedicated detectives who investigate these vicious crimes are known as the Special Victims Unit"

wer1 = wer(ref, hyp1)
wer2 = wer(ref, hyp2)
# print(wer1, ';', wer2)

# print(clean_extra_words(ref, hyp1))
