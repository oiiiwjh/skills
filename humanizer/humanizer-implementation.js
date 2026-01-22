/**
 * Humanizer Skill Implementation for OpenCode
 * Based on blader/humanizer (https://github.com/blader/humanizer)
 * 
 * Detects and removes 24 AI writing patterns to make text sound more human.
 */

class Humanizer {
  constructor(options = {}) {
    this.options = {
      strictness: 'medium', // low, medium, high
      preserveTone: true,
      addPersonality: true,
      targetAudience: 'general', // academic, business, casual, technical
      ...options
    };
    
    this.patterns = this.initializePatterns();
  }

  /**
   * Initialize all 24 AI writing patterns with detection rules and transformations
   */
  initializePatterns() {
    return {
      // Content Patterns (1-6)
      significanceInflation: {
        name: 'Significance Inflation',
        description: 'Undue emphasis on importance, legacy, and broader trends',
        keywords: [
          'pivotal moment', 'testament to', 'underscores its importance',
          'symbolizing its ongoing', 'marking a shift', 'evolving landscape',
          'vital role', 'crucial moment', 'key turning point', 'indelible mark',
          'deeply rooted', 'stands as', 'serves as'
        ],
        transform: (text) => text.replace(
          /(?:stands|serves) as (?:a )?(?:testament|reminder) to|(?:vital|significant|crucial|pivotal|key) (?:role|moment)|underscores? its (?:importance|significance)/gi,
          (match) => {
            // Replace with more neutral language
            if (match.toLowerCase().includes('testament')) return 'demonstrates';
            if (match.toLowerCase().includes('underscores')) return 'shows';
            return 'is important for';
          }
        )
      },

      notabilityNameDropping: {
        name: 'Notability Name-Dropping',
        description: 'Listing sources without context',
        keywords: ['cited in', 'media outlets', 'active social media presence'],
        transform: (text) => text.replace(
          /(?:cited|featured|mentioned) in (?:[A-Z][a-z]+(?:, | and )?)+/g,
          'mentioned in media'
        )
      },

      superficialIngAnalyses: {
        name: 'Superficial -ing Analyses',
        description: 'Tacking present participle phrases onto sentences',
        keywords: ['highlighting', 'underscoring', 'emphasizing', 'ensuring', 'reflecting', 'symbolizing', 'contributing to', 'cultivating', 'fostering', 'encompassing', 'showcasing'],
        transform: (text) => text.replace(
          /, (?:highlighting|underscoring|emphasizing|ensuring|reflecting|symbolizing|contributing to|cultivating|fostering|encompassing|showcasing) [^.,;]+[.,;]/gi,
          '.'
        )
      },

      promotionalLanguage: {
        name: 'Promotional Language',
        description: 'Advertisement-like, non-neutral tone',
        keywords: ['boasts a', 'vibrant', 'rich', 'profound', 'enhancing its', 'showcases', 'exemplifies', 'commitment to', 'natural beauty', 'nestled', 'in the heart of', 'groundbreaking', 'renowned', 'breathtaking', 'must-visit', 'stunning'],
        transform: (text) => text.replace(
          /(?:boasts a|vibrant|rich|profound|enhancing its|showcases|exemplifies|commitment to|natural beauty|nestled|in the heart of|groundbreaking|renowned|breathtaking|must-visit|stunning)/gi,
          (match) => {
            const replacements = {
              'boasts a': 'has',
              'vibrant': 'active',
              'rich': 'diverse',
              'profound': 'significant',
              'enhancing its': 'improving',
              'showcases': 'shows',
              'exemplifies': 'demonstrates',
              'commitment to': 'focus on',
              'natural beauty': 'scenery',
              'nestled': 'located',
              'in the heart of': 'in',
              'groundbreaking': 'innovative',
              'renowned': 'known',
              'breathtaking': 'impressive',
              'must-visit': 'worth visiting',
              'stunning': 'attractive'
            };
            return replacements[match.toLowerCase()] || match;
          }
        )
      },

      vagueAttributions: {
        name: 'Vague Attributions',
        description: 'Attributing opinions to vague authorities',
        keywords: ['Industry reports', 'Observers have cited', 'Experts argue', 'Some critics argue', 'several sources', 'publications'],
        transform: (text) => text.replace(
          /(?:Industry reports|Observers have cited|Experts argue|Some critics argue|several sources|publications)/gi,
          'Sources'
        )
      },

      formulaicChallenges: {
        name: 'Formulaic Challenges',
        description: 'Outline-like "Challenges and Future Prospects" sections',
        keywords: ['Despite its', 'faces several challenges', 'Despite these challenges', 'Challenges and Legacy', 'Future Outlook'],
        transform: (text) => text.replace(
          /Despite (?:its|these challenges)[^.,;]+continues to thrive/gi,
          'has challenges but continues'
        )
      },

      // Language Patterns (7-12)
      aiVocabulary: {
        name: 'AI Vocabulary',
        description: 'Overused "AI vocabulary" words',
        keywords: ['Additionally', 'align with', 'crucial', 'delve', 'emphasizing', 'enduring', 'enhance', 'fostering', 'garner', 'highlight', 'interplay', 'intricate', 'intricacies', 'key', 'landscape', 'pivotal', 'showcase', 'tapestry', 'testament', 'underscore', 'valuable', 'vibrant'],
        transform: (text) => text.replace(
          /\b(Additionally|align with|crucial|delve|emphasizing|enduring|enhance|fostering|garner|highlight|interplay|intricate|intricacies|key|landscape|pivotal|showcase|tapestry|testament|underscore|valuable|vibrant)\b/gi,
          (match) => {
            const replacements = {
              'additionally': 'also',
              'align with': 'match',
              'crucial': 'important',
              'delve': 'explore',
              'emphasizing': 'stressing',
              'enduring': 'lasting',
              'enhance': 'improve',
              'fostering': 'encouraging',
              'garner': 'gain',
              'highlight': 'emphasize',
              'interplay': 'interaction',
              'intricate': 'complex',
              'intricacies': 'complexities',
              'key': 'important',
              'landscape': 'environment',
              'pivotal': 'critical',
              'showcase': 'display',
              'tapestry': 'mix',
              'testament': 'proof',
              'underscore': 'emphasize',
              'valuable': 'useful',
              'vibrant': 'active'
            };
            return replacements[match.toLowerCase()] || match;
          }
        )
      },

      copulaAvoidance: {
        name: 'Copula Avoidance',
        description: 'Avoidance of simple "is"/"are" constructions',
        keywords: ['serves as', 'stands as', 'marks', 'represents', 'boasts', 'features', 'offers'],
        transform: (text) => text.replace(
          /\b(serves as|stands as|marks|represents|boasts|features|offers) (?:a )?/gi,
          (match) => {
            if (match.toLowerCase().includes('serves as') || 
                match.toLowerCase().includes('stands as') ||
                match.toLowerCase().includes('represents')) {
              return 'is ';
            }
            if (match.toLowerCase().includes('boasts') || 
                match.toLowerCase().includes('features') ||
                match.toLowerCase().includes('offers')) {
              return 'has ';
            }
            return match;
          }
        )
      },

      negativeParallelisms: {
        name: 'Negative Parallelisms',
        description: 'Constructions like "Not only...but..." or "It\'s not just..."',
        keywords: ['not only', 'but also', 'it\'s not just', 'it\'s not merely', 'it\'s'],
        transform: (text) => text.replace(
          /(?:It'?s not (?:just|merely|only) (?:about )?)?([^.,;]+?),? (?:it'?s|but (?:also)?) ([^.,;]+?)[.,;]/gi,
          '$1 and $2.'
        )
      },

      ruleOfThree: {
        name: 'Rule of Three',
        description: 'Forcing ideas into groups of three',
        transform: (text) => {
          // This is more complex - would need NLP to detect forced triplets
          return text.replace(
            /(\w+), (\w+), and (\w+)/gi,
            (match, p1, p2, p3) => {
              // Only apply if the three items seem forced/unnatural
              // For now, just return as-is
              return match;
            }
          );
        }
      },

      synonymCycling: {
        name: 'Synonym Cycling',
        description: 'Excessive synonym substitution',
        transform: (text) => {
          // This would require more advanced NLP
          // For now, return text unchanged
          return text;
        }
      },

      falseRanges: {
        name: 'False Ranges',
        description: '"from X to Y" where X and Y aren\'t on a meaningful scale',
        keywords: ['from', 'to'],
        transform: (text) => text.replace(
          /from ([^.,;]+?) to ([^.,;]+?)(?=[.,;])/gi,
          (match, p1, p2) => {
            // Check if p1 and p2 are on same scale
            // For now, convert to list
            return `${p1} and ${p2}`;
          }
        )
      },

      // Style Patterns (13-18)
      emDashOveruse: {
        name: 'Em Dash Overuse',
        description: 'Excessive use of em dashes',
        transform: (text) => text.replace(/—/g, ', ')
      },

      boldfaceOveruse: {
        name: 'Boldface Overuse',
        description: 'Mechanical use of boldface emphasis',
        transform: (text) => text.replace(/\*\*([^*]+)\*\*/g, '$1')
      },

      inlineHeaderLists: {
        name: 'Inline-Header Lists',
        description: 'Lists where items start with bolded headers',
        transform: (text) => text.replace(
          /- \*\*([^*]+)\*\*: ([^\n]+)/g,
          (match, header, content) => {
            return `${content.charAt(0).toUpperCase() + content.slice(1)}.`;
          }
        )
      },

      titleCaseHeadings: {
        name: 'Title Case Headings',
        description: 'Capitalizing all main words in headings',
        transform: (text) => text.replace(
          /^#+ (.+)$/gm,
          (match, heading) => {
            // Convert to sentence case
            return match.replace(heading, heading.toLowerCase());
          }
        )
      },

      emojis: {
        name: 'Emojis',
        description: 'Decorating headings or bullet points with emojis',
        transform: (text) => text.replace(
          /[^\w\s.,;:!?()\[\]{}'"-]/g, // Remove most non-alphanumeric characters
          ''
        ).replace(/\s+/g, ' ').trim()
      },

      curlyQuotes: {
        name: 'Curly Quotes',
        description: 'Using curly quotes instead of straight quotes',
        transform: (text) => text.replace(/[""]/g, '"').replace(/['']/g, "'")
      },

      // Communication Patterns (19-21)
      chatbotArtifacts: {
        name: 'Chatbot Artifacts',
        description: 'Text meant as chatbot correspondence',
        keywords: ['I hope this helps', 'Of course', 'Certainly', 'You\'re absolutely right', 'Would you like', 'let me know', 'here is a'],
        transform: (text) => text.replace(
          /(?:I hope this helps|Of course!|Certainly!|You'?re absolutely right!|Would you like|let me know|here is a)[^.,;]*[.,;]/gi,
          ''
        ).trim()
      },

      cutoffDisclaimers: {
        name: 'Knowledge-Cutoff Disclaimers',
        description: 'Disclaimers about incomplete information',
        keywords: ['as of', 'Up to my last training update', 'While specific details are limited', 'based on available information'],
        transform: (text) => text.replace(
          /(?:as of|Up to my last training update|While specific details are limited|based on available information)[^.,;]*[.,;]/gi,
          ''
        ).trim()
      },

      sycophanticTone: {
        name: 'Sycophantic Tone',
        description: 'Overly positive, people-pleasing language',
        keywords: ['Great question', 'excellent point', 'wonderful insight'],
        transform: (text) => text.replace(
          /(?:Great question|excellent point|wonderful insight)[^.,;]*[.,;]/gi,
          ''
        ).trim()
      },

      // Filler and Hedging (22-24)
      fillerPhrases: {
        name: 'Filler Phrases',
        description: 'Unnecessary wordy phrases',
        patterns: [
          { from: 'in order to', to: 'to' },
          { from: 'due to the fact that', to: 'because' },
          { from: 'at this point in time', to: 'now' },
          { from: 'in the event that', to: 'if' },
          { from: 'has the ability to', to: 'can' },
          { from: 'it is important to note that', to: '' }
        ],
        transform: (text) => {
          let result = text;
          this.patterns.fillerPhrases.patterns.forEach(pattern => {
            const regex = new RegExp(pattern.from, 'gi');
            result = result.replace(regex, pattern.to);
          });
          return result;
        }
      },

      excessiveHedging: {
        name: 'Excessive Hedging',
        description: 'Over-qualifying statements',
        transform: (text) => text.replace(
          /(?:could potentially possibly|might possibly|may potentially)/gi,
          'may'
        )
      },

      genericConclusions: {
        name: 'Generic Positive Conclusions',
        description: 'Vague upbeat endings',
        keywords: ['The future looks bright', 'Exciting times lie ahead', 'journey toward excellence', 'major step in the right direction'],
        transform: (text) => text.replace(
          /(?:The future looks bright|Exciting times lie ahead|journey toward excellence|major step in the right direction)[^.,;]*[.,;]/gi,
          ''
        ).trim()
      }
    };
  }

  /**
   * Process text to remove AI writing patterns
   */
  async humanize(text) {
    if (!text || typeof text !== 'string') {
      throw new Error('Input must be a non-empty string');
    }

    let result = text;
    const detectedPatterns = [];
    const changes = [];

    // Apply each pattern transformation
    for (const [patternKey, pattern] of Object.entries(this.patterns)) {
      const original = result;
      result = pattern.transform(result);
      
      if (result !== original) {
        detectedPatterns.push(patternKey);
        changes.push({
          pattern: pattern.name,
          description: pattern.description,
          changesMade: this.diffText(original, result)
        });
      }
    }

    // Add personality if requested
    if (this.options.addPersonality) {
      result = this.addPersonality(result);
    }

    // Adjust for target audience
    result = this.adjustForAudience(result);

    return {
      original: text,
      humanized: result,
      detectedPatterns,
      changes,
      summary: this.generateSummary(detectedPatterns, changes)
    };
  }

  /**
   * Add human personality to text
   */
  addPersonality(text) {
    // Simple personality injection - can be expanded
    const sentences = text.split(/[.!?]+/).filter(s => s.trim());
    
    if (sentences.length > 3) {
      // Vary sentence length
      const variedSentences = sentences.map((sentence, index) => {
        const trimmed = sentence.trim();
        if (index % 3 === 0 && trimmed.length > 50) {
          // Split long sentences
          const parts = trimmed.split(',');
          if (parts.length > 2) {
            return parts.slice(0, 2).join(',') + '. ' + parts.slice(2).join(',');
          }
        }
        return trimmed;
      });
      
      return variedSentences.join('. ').replace(/\s+/g, ' ').trim() + '.';
    }
    
    return text;
  }

  /**
   * Adjust text for target audience
   */
  adjustForAudience(text) {
    switch (this.options.targetAudience) {
      case 'academic':
        return text.replace(/I think/g, 'The evidence suggests')
                   .replace(/I believe/g, 'It appears that');
      case 'business':
        return text.replace(/maybe/g, 'potentially')
                   .replace(/I think/g, 'analysis indicates');
      case 'casual':
        return text.replace(/analysis indicates/g, 'I think')
                   .replace(/it appears that/g, 'it seems like');
      default:
        return text;
    }
  }

  /**
   * Generate summary of changes
   */
  generateSummary(detectedPatterns, changes) {
    if (detectedPatterns.length === 0) {
      return 'No AI writing patterns detected. Text appears human-written.';
    }

    const patternCount = detectedPatterns.length;
    const categories = {
      content: detectedPatterns.filter(p => p.includes('Inflation') || p.includes('Promotional') || p.includes('Vague')).length,
      language: detectedPatterns.filter(p => p.includes('Vocabulary') || p.includes('Copula') || p.includes('Parallel')).length,
      style: detectedPatterns.filter(p => p.includes('Dash') || p.includes('Boldface') || p.includes('Emoji')).length,
      communication: detectedPatterns.filter(p => p.includes('Chatbot') || p.includes('Cutoff') || p.includes('Sycophantic')).length,
      filler: detectedPatterns.filter(p => p.includes('Filler') || p.includes('Hedging') || p.includes('Generic')).length
    };

    const activeCategories = Object.entries(categories)
      .filter(([_, count]) => count > 0)
      .map(([cat]) => cat);

    return `Detected ${patternCount} AI writing patterns across ${activeCategories.length} categories: ${activeCategories.join(', ')}.`;
  }

  /**
   * Simple text diff for change tracking
   */
  diffText(original, modified) {
    if (original === modified) return [];
    
    const originalWords = original.split(/\s+/);
    const modifiedWords = modified.split(/\s+/);
    const changes = [];
    
    for (let i = 0; i < Math.max(originalWords.length, modifiedWords.length); i++) {
      if (originalWords[i] !== modifiedWords[i]) {
        changes.push({
          position: i,
          original: originalWords[i] || '',
          modified: modifiedWords[i] || ''
        });
      }
    }
    
    return changes.slice(0, 5); // Return first 5 changes
  }

  /**
   * Batch process multiple texts
   */
  async batchHumanize(texts) {
    const results = [];
    for (const text of texts) {
      results.push(await this.humanize(text));
    }
    return results;
  }

  /**
   * Get statistics about processed text
   */
  getStatistics(text, humanizedText) {
    const originalWords = text.split(/\s+/).length;
    const humanizedWords = humanizedText.split(/\s+/).length;
    const originalChars = text.length;
    const humanizedChars = humanizedText.length;
    
    return {
      wordCount: { original: originalWords, humanized: humanizedWords },
      charCount: { original: originalChars, humanized: humanizedChars },
      reduction: {
        words: ((originalWords - humanizedWords) / originalWords * 100).toFixed(1) + '%',
        chars: ((originalChars - humanizedChars) / originalChars * 100).toFixed(1) + '%'
      },
      readability: this.calculateReadability(humanizedText)
    };
  }

  /**
   * Calculate readability score (simplified)
   */
  calculateReadability(text) {
    const sentences = text.split(/[.!?]+/).filter(s => s.trim());
    const words = text.split(/\s+/);
    const syllables = this.estimateSyllables(text);
    
    if (sentences.length === 0 || words.length === 0) return 0;
    
    // Simple Flesch Reading Ease approximation
    const wordsPerSentence = words.length / sentences.length;
    const syllablesPerWord = syllables / words.length;
    
    return Math.max(0, Math.min(100, 206.835 - (1.015 * wordsPerSentence) - (84.6 * syllablesPerWord)));
  }

  /**
   * Estimate syllables in text
   */
  estimateSyllables(text) {
    const words = text.toLowerCase().split(/\s+/);
    let syllableCount = 0;
    
    words.forEach(word => {
      // Simple syllable estimation
      syllableCount += word.length > 6 ? 3 : word.length > 3 ? 2 : 1;
    });
    
    return syllableCount;
  }
}

// Export for use in OpenCode
module.exports = Humanizer;

// Example usage
if (require.main === module) {
  const humanizer = new Humanizer();
  
  const exampleText = `The new software update serves as a testament to the company's commitment to innovation. Moreover, it provides a seamless, intuitive, and powerful user experience—ensuring that users can accomplish their goals efficiently. It's not just an update, it's a revolution in how we think about productivity. Industry experts believe this will have a lasting impact on the entire sector, highlighting the company's pivotal role in the evolving technological landscape.`;
  
  humanizer.humanize(exampleText).then(result => {
    console.log('Original:', result.original);
    console.log('\nHumanized:', result.humanized);
    console.log('\nSummary:', result.summary);
    console.log('\nDetected patterns:', result.detectedPatterns.length);
  });
}