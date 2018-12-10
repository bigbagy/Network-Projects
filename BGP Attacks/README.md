# BGP hijacking Attack

Explored some of the vulnerabilities of Border Gateway Protocol (BGP). 

In particular, how BGP is vulnerable to abuse and manipulation through BGP hijacking attacks.

A malicious Autonomous System (AS) can mount these attacks through false BGP announcements from a rogue AS, causing victim ASes to route their traffic bound for another AS through the malicious AS. 

This code simulates the process of false advertisements exploiting BGP routing behavior by advertising a shorter path to reach a particular prefix, which causes victim ASes to attempt to use the newly advertised (and seemingly better) route.
