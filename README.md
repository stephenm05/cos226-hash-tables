# cos226-hash-tables
<h2>Reflection</h2>
<p>All of the implementations tested for this assignment used a hash table size equal to the number of entries to be added, so there were always 0 unused slots. While larger hash tables were briefly examined, they generally increased collisions, in addition to necessarily having empty slots, and so they weren't used. A brief summary of each implementation's approach is given below:</p>
<ul>
<li>HF1: Just interpret the binary data in the provided string as a number, used as a baseline because of its computational simplicity</li>
<li>HF2: Bisect and swap string data before interpreting as a number to break up end-of-word patterns</li>
<li>HF3: Interpret the string as a number, square it, and extract a more reasonably-sized number from the square's central digits to propogate small differences in each string provided</li>
<li>HF4: Interpret the string as a series of numbers and sum them together, rather than interpreting as one large number, to make the output less dependent on string length</li>
<li>HF5: Interpret the string as one number and mod it by a rough multiple of the table size to ensure the hash function's range of outputs doesn't favor one end of the allowed index range over the other</li>
</ul>
<p>In terms of collisions, the final implementations chosen don't display that much variance, with the lowest collision statistic for both the title and quote tables barely being 100 collisions better than the worst statistic for each. While substantially worse collision statistics (in the 12-14k range) were encountered over the course of this assignment, not much improvement over HF1, likely the simplest and therefor fastest means by which string data can be turned into an int by a computer, was found. The performance rankings in terms of collisions for each type of table are given below:</p>
<b>Title</b>
<ol>
<li>HF5: 6,983</li>
<li>HF1: 7,009</li>
<li>HF4: 7,024</li>
<li>HF3: 7,058</li>
<li>HF2: 7,086</li>
</ol>
<br>
<b>Quote</b>
<ol>
<li>HF5: 5,499</li>
<li>HF3: 5,549</li>
<li>HF2: 5,554</li>
<li>HF4: 5,562</li>
<li>HF1: 5,603</li>
</ol>
<p>As can be seen from this data, HF5 was overall the most effective hashing method, likely because it most-explicitly ensured its range of outputs could be modded to conform to the table size without creating an un-uniform distribution of indexes. The other methods left their output ranges essentially random, and so values towards the upper end of those ranges likely tended to get shoved into lower indexes by the post-hash function mod. Comparing time values even on the same computer is dubious, since the things going on on that machine besides the program that's timing itself affect how uninterrupted that program will be in performing its operations, but both tables did have relatively low construction times with HF5, essentially the same as those for HF1. Due to the overall low variance in collision data, though, HF5's apparent supremacy over the other approaches tried here should be taken with a grain of salt. As can be seen in how much the rankings of the subsequent hash function implementations for each table differ, the contents of the data supplied to the hash function matter a great deal in determining how uniformly that function will map it to a range of indexes, and so all of the implementations recorded here could likely make good hash functions when applied to an appropriate data set. The important thing is to try a variety of approaches and see which actually works best in a particular situation, rather than simply memorizing one algorithm and assuming its performance is universal.</p>