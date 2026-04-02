How far did the agent get? Did it fully implement your spec? What percentage of your acceptance criteria passed on the first try?

It tried and claimed it did implement the entire program, but only 12/20 = 60%  of the acceptence criteria passed on the first try. I was not particularly impressed with how far the agent got. 



Where did you intervene? List each time you had to step in during Phase 2. Why was the intervention needed? Could a better spec have prevented it?

The agent worked so quickly that I'm not sure what I could've done to intervene. The only input I gave it was approving some pwsh commands. 



How useful was the AI review? Did it catch real bugs? Did it miss anything important? Did it flag things that weren't actually problems?

The AI review was somewhat helpful but missed some important things. The most annoying issue was that the question bank was not properly completed. The minimum amount of questions per catergory and difficulty were not reached so I had to add several more questions myself. Many of AI generated questions were innaccurate and terrible by the way. A questionable 'issue' it identified was that if one of the critical files is somehow deleted while the program is running then it would crash, and I'm skeptical if that is really a problem - how could it not crash if that happened? It did seem to identify some security issues with the usage of pickle. It also had some sort of problem with the 'I give up.' feature and the login part of the program, and I honestly couldn't actually understand its description of the issue.    



Spec quality → output quality: In hindsight, what would you change about your spec to get a better result from the agent?

I don't know and I want to talk to Mike about it in OH. I wrote a pretty long and detailed spec, and it seemed to be much larger than some of my peers who apparently ended up with better results. So I don't know. 



When would you use this workflow? Based on this experience, when do you think plan-delegate-review is better than conversational back-and-forth? When is it worse?

I didn't get great results from this, so I'm not sure if I would ever use this workflow. Maybe if it turns out I didn't do it right I could try again. Based on this experience, the time spent writing a detailed spec negated the time saved by letting the agents do most of the heavy lifting once the spec was complete. The workflow I've used before where I consult the AI on the plan and implementation of each necessary part of the program is just about the same amount of time and effort but gave me better results. 

