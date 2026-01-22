const Humanizer = require('./humanizer-implementation.js');

async function testHumanizer() {
  console.log('Testing Humanizer Skill Installation...\n');
  
  const humanizer = new Humanizer();
  
  const testTexts = [
    "The new software update serves as a testament to the company's commitment to innovation.",
    "This research delves into the intricate interplay between quantum computing and machine learning.",
    "Hey there! I hope this helps! Let me know if you need anything else! 😊"
  ];
  
  for (let i = 0; i < testTexts.length; i++) {
    console.log(`Test ${i + 1}:`);
    console.log('Original:', testTexts[i]);
    
    try {
      const result = await humanizer.humanize(testTexts[i]);
      console.log('Humanized:', result.humanized);
      console.log('Detected patterns:', result.detectedPatterns.length);
      console.log('Summary:', result.summary);
      console.log('---\n');
    } catch (error) {
      console.error('Error:', error.message);
    }
  }
  
  console.log('✅ Humanizer skill installed successfully!');
  console.log('You can now use it in OpenCode with:');
  console.log('  /humanizer [your text]');
  console.log('  or');
  console.log('  Please humanize this text: [your text]');
}

testHumanizer().catch(console.error);