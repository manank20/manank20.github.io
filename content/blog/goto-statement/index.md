+++
title = "The \"goto\" statement"
description = "A brief history of the goto construct in C programming."
date = 2023-12-06T23:30:20+05:30
authors = ["Manank"]

[taxonomies]
categories = ["Articles"]
tags = ["Programming", "C", "History"]

[extra]
toc = true
comments = true
+++

The goto statement has been controversial since the advent of programming languages. In this blog post, we will deep dive into the history and the origin of the
sentiment(yes, it is Dijkstra!), and the opposing views and the rationality behind both.

<!-- more -->
### Introduction
A "goto" statement is like a magical teleporter in computer programming. It lets the computer jump from one part of a program to another without any conditions or questions. Imagine it's like a super-fast shortcut that programmers can use to change the usual order of instructions. It's beautiful. In assembly language, it is a single jump instruction.

<center>
  <img src="/images/goto.png" width=500 alt="goto"/>
</center>

### Motivation
So we had a course called Computer Networks, and as a part of that, we had a few labs and assignments. One day, I was writing code(in C), and my friend 
came into my room, stared at my screen, and then said, "Bruh, you are using goto?! Don't use it; it's not good.". I asked him why, and he gave various good 
reasons for it, which we will discuss further, but still, I was not convinced because where I had used goto, it made a lot of sense, and I had seen 
a lot of gotos in the Linux kernel code. As far as I remember, I had used it to break out of a triple loop and resource cleaning in case of error. So, I 
decided to dig deeper and find out more about this debate.

### Dijkstra's Thoughts
Dijkstra published a relatively strong article against the use of goto in The Communications of the ACM 11, 3 (March 1968), [Go To Statement Considered Harmful](dij.pdf).

<center>
  <img src="/images/Edsger_Dijkstra.jpg" width=200 alt="goto"/>
</center>

> Edsger Dijkstra was a Dutch computer scientist who made significant contributions to the fields of algorithms, programming, and software engineering. His work on the Dijkstra algorithm, structured programming, and formal methods has had a lasting impact on the field. 

> Fun fact about the Title: The original title of the article was [EWD 215: A Case against the GO TO Statement](https://www.cs.utexas.edu/users/EWD/ewd02xx/EWD215.PDF). XYZ considered harmful was a common title during that time, and thus it was published with the current title. 

The majority of the opposition to the goto construct among students, professors, and other programmers comes from this paper. Which is valid as long as you
have read the entire article. The majority of people today will agree that they should avoid gotos at all costs, but hardly a few will be able to answer
that "why" should you do that. There is also a famous quote at the beginning of the article that goes like this:-
> The quality of programmers is a decreasing function of the density of goto statements in the programs they produce.

A powerful statement to make; he goes on to say that he is convinced that the goto statement should be abolished from all "higher level" programming
languages. Keep in mind that at the time of publication, C did not even exist.
One of the points that Dijkstra focused on was about the structure of the program. He argued that the extensive use of gotos in a program makes it harder
for the reader to understand and maintain. Imagine a function spanning 1000 lines and a goto statement from, say, line 200 down to 800 and many other
similar jumps; it's very easy to get confused and lose track of all the branching, which is the result of several goto statements.

The main motive of Dijkstra seems to encourage the use of a structured programming paradigm.

#### Structured Programming
According to Dijkstra's [Notes on Structured Programming](notes-on-structured.pdf), He defines structured programming as a method of writing programs that uses a limited set of control structures. He argues that this approach makes programs easier to understand, maintain, and modify. He identifies three basic control structures: sequence, selection, and iteration. He also discusses the importance of using recursion and data abstraction.

Specifically, Dijkstra argues that structured programming can help to avoid the "spaghetti code" problem, in which programs become difficult to
understand and maintain due to their complex and tangled structure. He suggests that by using a limited set of control structures, programmers can make 
their programs more modular and easier to reason about.

Dijkstra also discusses the importance of using recursion and data abstraction in structured programming. Recursion is a technique in which a function 
calls itself. This can be a powerful tool for writing concise and elegant programs. Data abstraction is the process of hiding the implementation details 
of a data structure or algorithm. This can make programs easier to understand and maintain, as programmers can focus on the functionality of the program 
without having to worry about the underlying details.

So basically, structured programming aims to make the structure of the program easier to read and less confusing by following a single entry, single 
exit principle, and thus discourages the usage of goto, which would break the principle.


### Responses to the Article
There have been a few responses to the article in the form of publications and many debates and arguments in various online forums.
The most widely studied and sought-after response is by none other than [Donald Knuth](https://en.wikipedia.org/wiki/Donald_Knuth).


<center>
  <img src="/images/knuth.jpg" width=300 alt="goto"/>
</center>

> Donald Knuth, a towering figure in computer science, is renowned for his seminal work on algorithms, his revolutionary TeX typesetting system, and his influential multi-volume series "The Art of Computer Programming." A Turing Award winner, Knuth's meticulousness and passion for clarity have shaped modern computing, making him a legend in the field.

#### Structured Programming with GOTO statements by Donald E. Knuth
Knuth did defend the judicious usage of goto in [Structured Programming with GOTO](knuth-GOTO.pdf). I suggest you give it a read. He argued that 
there are cases where the "goto" statement can enhance code expressiveness. He gave 
examples of situations where using "goto" could lead to more concise and efficient code. He also contended that in some instances, using "goto" could 
lead to more explicit and more efficient code, particularly in situations involving error handling and resource cleanup, which is a common pattern in kernel
code. 

#### Examples
Here are a few examples from a [stackoverflow thread](https://softwareengineering.stackexchange.com/questions/154974/is-this-a-decent-use-case-for-goto-in-c/154980#154980)
The OP posted the following code, which is the case when we try to avoid gotos; it becomes a mess if there are multiple
functions that could fail and could lead to 5-6 levels of indentation.
```c
error = function_that_could_fail_1();
if (!error) {
    error = function_that_could_fail_2();
    if (!error) {
        error = function_that_could_fail_3();
        if(!error) {
          error = function_that_could_fail_4();
          if(!error){
              ...to the n-th tab level!
          } else {
                // deal with error, clean up, and return error code
          }
        } else {
            // deal with error, clean up, and return error code
        }
    } else {
        // deal with error, clean up, and return error code
    }
} else {
    // deal with error, clean up, and return error code
}
```
But if we decide to use goto, the solution is much more simple, elegant, and readable
```c
error = function_that_could_fail_1();
if(error) {
    goto cleanup;
}
error = function_that_could_fail_2();
if(error) {
    goto cleanup;
}
error = function_that_could_fail_3();
if(error) {
    goto cleanup;
}
...
cleanup:
// deal with error if it exists, clean up
// return error code
```
another similar snippet
```c
int frobnicateTheThings() {
    char *workingBuffer = malloc(...);
    int i;

    for (i=0 ; i<numberOfThings ; i++) {
        if (giveMeThing(i, workingBuffer) != OK)
            goto error;
        if (processing(workingBuffer) != OK)
            goto error;
        if (dispatching(i, workingBuffer) != OK)
            goto error;
    }

    free(workingBuffer);
    return OK;

  error:
    free(workingBuffer);
    return OOPS;
}
```
This is one of the examples where using goto makes the code more readable. `goto`s become confusing when the
jumps are bi-directional, but using one-way jumps in situations like this can improve the overall readability
and encourage code reuse. The same code without the use of goto would look like this:-


```c
int frobnicateTheThings() {
    char *workingBuffer = malloc(...);
    int i;

    for (i=0 ; i<numberOfThings ; i++) {
        if (giveMeThing(i, workingBuffer) != OK){
          free(workingBuffer);
          return OOPS;
        }
        if (processing(workingBuffer) != OK){
          free(workingBuffer);
          return OOPS;
        }
        if (dispatching(i, workingBuffer) != OK){
          free(workingBuffer);
          return OOPS;
        }
    }

    free(workingBuffer);
    return OK;
}
```

Another argument for the use of goto statements might be performance, as explained in this [20-year-old thread on Linux kernel mailing list](https://lkml.org/lkml/2003/1/12/203)

> Subject Re: any chance of 2.6.0-test*? </br>
> From: Robert Love </br>
> Date: 12 Jan 2003 17:58:06 -0500 </br>
>
> On Sun, 2003-01-12 at 17:22, Rob Wilkens wrote:
>
>> I say "please don't use goto" and instead have a "cleanup_lock" function
>> and add that before all the return statements..  It should not be a
>> burden.  Yes, it's asking the developer to work a little harder, but the
>> end result is better code.
>
>No, it is gross and it bloats the kernel.  It inlines a bunch of junk
>for N error paths, as opposed to having the exit code once at the end. 
>Cache footprint is key, and you just killed it.
>
>Nor is it easier to read.
>
>As a final argument, it does not let us cleanly do the usual stack-esque
>wind and unwind, i.e.
>
>```c
> do A
> if (error)
>   goto out_a;
> do B
> if (error)
>   goto out_b;
> do C
> if (error)
>   goto out_c;
> goto out;
> out_c:
> undo C
> out_b:
> undo B:
> out_a:
> undo A
> out:
> return ret;
>```
>
>Now stop this.
>
> Robert Love

That being said, it is very tempting to use gotos when it is not required and create spaghetti code; thus programmers
should really know what they are doing when they decide to use goto.

A lot of times, the usage of break and continue in C might also need to be clarified, as it is difficult to predict the flow in case
of multiple nested loops with multiple conditions. Also, the capabilities of break and continue are limited, such that
breaking out from multiple nested loops is impossible to do without `goto`. It also gives more granular control
in case of multiple nested loops so as to break out of, let's say 2 inner loops instead of only, say only, the innermost loop,
which is the case with `break.`



### Conclusion
So then, should you use `goto` or not? Well, it depends, actually. If you are using a higher-level programming language than C, the chances
are that you might never need to think about it, there would be better structured programming constructs offered by your language.
But then there are languages like lisp that rely heavily on `goto`s. 
If you are using C, then it gets difficult to gauge the feasibility and the effect of using `goto` such that it improves the overall
quality and readability of the code, but not so much that it results in spaghetti code.

> “as a full professor with tenure, I don't have to worry about being fired when I use goto statements.” — Donald Knuth :-) 