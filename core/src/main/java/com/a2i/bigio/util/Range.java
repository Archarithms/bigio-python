/*
 * Copyright (c) 2014, Archarithms Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer. 
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * The views and conclusions contained in the software and documentation are those
 * of the authors and should not be interpreted as representing official policies, 
 * either expressed or implied, of the FreeBSD Project.
 */

package com.a2i.bigio.util;

/**
 * This class is a numeric range.  It handles both inclusive and exclusive 
 * bounds.
 * 
 * @author Andy Trimble
 */
public class Range {
    private final double upperBound;
    private final double lowerBound;

    private boolean upperInclusive = false;
    private boolean lowerInclusive = false;

    /**
     * Create the numeric range (lowerBound, upperBound).
     * 
     * @param lowerBound the lower bound (assumed to be exclusive).
     * @param upperBound the upper bound (assumed to be exclusive).
     */
    public Range(double lowerBound, double upperBound) {
        if(lowerBound > upperBound) {
            double tmp = lowerBound;
            lowerBound = upperBound;
            upperBound = tmp;
        }
        
        this.lowerBound = lowerBound;
        this.upperBound = upperBound;
    }

    /**
     * Create a numeric range with the specified bounds and the specified
     * exclusivity.
     * 
     * @param lowerBound the lower bound.
     * @param upperBound the upper bound.
     * @param lowerInclusive true if the lower bound is inclusive.
     * @param upperInclusive true if the upper bound is inclusive.
     */
    public Range(double lowerBound, double upperBound, boolean lowerInclusive, boolean upperInclusive) {
        if(lowerBound > upperBound) {
            double tmp = lowerBound;
            lowerBound = upperBound;
            upperBound = tmp;
        }
            
        this.lowerBound = lowerBound;
        this.upperBound = upperBound;
        this.lowerInclusive = lowerInclusive;
        this.upperInclusive = upperInclusive;
    }

    /**
     * Construct a numeric range from the supplied string.  The string must be
     * of the format "( or [ number, number ] or )".  If a bound is specified
     * with a bracket, then the bound is inclusive.  If a bound is specified
     * with a parenthesis, then the bound is exclusive.
     * 
     * @param range a range string.
     * @throws NumberFormatException if the range is ill defined.
     */
    public Range(String range) throws NumberFormatException {
        String[] spl = range.trim().split(",");
        if(spl.length != 2) {
            throw new NumberFormatException("Not a valid range of the form (x, y) or [x, y]");
        }

        if(spl[0].charAt(0) == '[') {
            lowerInclusive = true;
        } else if(spl[0].charAt(0) == '(') {
            lowerInclusive = false;
        } else {
            throw new NumberFormatException("Not a valid range of the form (x, y) or [x, y]");
        }
        if(spl[1].charAt(spl[1].length() - 1) == ']') {
            upperInclusive = true;
        } else if(spl[1].charAt(spl[1].length() - 1) == ')') {
            upperInclusive = false;
        } else {
            throw new NumberFormatException("Not a valid range of the form (x, y) or [x, y]");
        }

        double tempLowerBound = Double.parseDouble(spl[0].substring(1));
        double tempUpperBound = Double.parseDouble(spl[1].substring(0, spl[1].length() - 1));

        if(tempLowerBound > tempUpperBound) {
            double tmp = tempLowerBound;
            tempLowerBound = tempUpperBound;
            tempUpperBound = tmp;
        }

        lowerBound = tempLowerBound;
        upperBound = tempUpperBound;
    }

    /**
     * Determine if a number is within this range.
     * 
     * @param number a number.
     * @return true if the number is within this range, false otherwise.
     */
    public boolean contains(Number number) {
        return (upperInclusive ? number.doubleValue() <= upperBound : number.doubleValue() < upperBound) && 
                (lowerInclusive ? number.doubleValue() >= lowerBound : number.doubleValue() > lowerBound);
    }

    /**
     * Get the lower bound of this range.
     * 
     * @return the lower bound.
     */
    public double getLowerBound() {
        return lowerBound;
    }

    /**
     * Get the upper bound of this range.
     * 
     * @return the upper bound.
     */
    public double getUpperBound() {
        return upperBound;
    }

    /**
     * Produce a nicely formatted string representing this range.
     * 
     * @return a string.
     */
    @Override
    public String toString() {
        return (lowerInclusive ? "[" : "(") + lowerBound + ", " + upperBound + (upperInclusive ? "]" : ")");
    }
}