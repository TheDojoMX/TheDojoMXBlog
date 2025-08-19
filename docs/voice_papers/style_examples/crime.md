The researchers in this study wanted to compile a database of police-reports, and then group those reports by the type of crime-scene described within each document. Seems simple enough, no?

Unfortunately the authors immediately hit a wall: It turns out that police reports contain so much sensitive and private information that they’re rarely made public. So the authors couldn't get their hands on any of them and had to figure out a workaround: Rather than deal directly with police reports, they would use public court documents instead. Their theory was that court documents often have the narrative-areas of the relevant police-reports embedded within them (literally copied and pasted from the police reports right into the court docs). So the researchers could still build a database of police-writing, they'd just have to get that writing from court documents instead of directly from the police reports.

With that strategy in place they downloaded the Caselaw Access Project database from Harvard Law School. This left them with approximately seven million cases. They were only interested in cases that concerned certain types of crimes, so they needed to narrow down this group significantly. They decided that a term-frequency analysis would be the best way to help them filter-down to just the cases they were interested in. They chose TF-IDF with K-means clustering, and ran it for a subset of the documents. Unfortunately that's where they hit the second wall.

The results of TF-IDF were unusable. For any given court file, there was a hundred or more pages of text, and the crime scene description was only a few paragraphs, buried somewhere deep in there. The rest of each document was procedural court filings and background information. So, rather than showing them the frequency of terms that were relevant to the crime-scene, the TF-IDF surfaced keywords that had more to do with each case’s procedural and appellate history.  
​  
Faced with this challenge they went back to the drawing board and built a novel classification pipeline. The pipeline they designed has four main steps:

1. Creation of a "crime dictionary"  
2. Preprocessing of the court docs  
3. Inference with a "Crime Scene Existence" model  
4. Inference with a "Crime Type" model.

Let’s start with the dictionary. The authors manually created a list of words that correlate highly with each of the crimes and crime-scenes they wanted to focus on. They called this list of words the "dictionary". Once this dictionary existed, they performed lemmatization on all the words. This means that they normalized the tenses, conjugations and forms of each word down to a common base. So, for example, if the words “stabbing”, and "stabbed" appeared in the text they would both be reduced to “stab”.

After their dictionary was complete, they ran two sets of pre-processes on the court documents.

1. They ran the same lemmatization on the docs that they did on the dictionary  
2. They re-ran TF-IDF on each of the case files, but this time with a difference: Instead of calculating word-frequencies for all the words in the document, they only focused on the subset of words in the dictionary. All the other words in the files were ignored.

Next, they trained a train a two-step classifier (consisting of two discrete models).

* They called the first model a Crime Scene Existence (CSE) classifier. It checks to see if the documents contain the description of a crime scene associated with any of the types of crimes they wanted to focus on.  
* They called the second model a Crime Type (CT) classifier. This would only run if the CSE classifier returned a positive result. The CT determines the label to apply to each doc (concerning the type of crime).

During model training they tried a number of different algorithms for each model. They analyzed the performance of each algorithm by looking at precision, sensitivity, specificity and f1 Score. Based on these metrics Random Forest (RF) was the best performer for the CSE model (90% accuracy) and Support Vector Machine (SVM) was the winner for the CT model (82% accuracy)

So what can we learn from this technique? I think quite a bit. As ML expands into more and more fields (like law for instance), we as practitioners are going to encounter more and more unstructured data. Sometimes that data will be easy to parse, sometimes not. Sometimes the information we want to extract will be prominent and in other cases it will be buried deep within files. When the latter happens, the tools we’re all used to (like TF-IDF) can’t be expected to give us the results we need.

This paper adds a new tool to our toolkit, useful for when we find ourselves in that kind of situation. A technique that lets us narrow down the noise and focus on the signal. Its drawback is obviously that it’s such a manual process and the dictionary requires either domain-expertise, or the willingness to acquire it. So it’s certainly not a general-purpose tool and won’t necessarily scale to fit larger problems. But for narrow cases where nothing else is working, creating your own custom dictionary might just be the solution you need.

If you’d like to learn more about how they performed their analysis or built their dictionary. Or if you’re a true-crime aficionado and want to read the details about the types of crimes they were studying (that I’ve gone out of my way not to mention explicitly during this episode) you should download the paper.

