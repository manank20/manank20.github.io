+++
title = "My kernel testing workflow"
description = "Setting up a minimal qemu vm for testing new kernel after compilation"
date = 2023-03-01T01:03:44+05:30
authors = ["Manank"]
draft=true

[taxonomies]
categories = ["Guide"]
tags = ["Kernel", "Development", "Linux"]

[extra]
toc = true
+++

Testing the new compiled kernel on the machine you are currently using is a big no-no.
Then how do you make sure it runs properly? qemu!

<!-- more -->
