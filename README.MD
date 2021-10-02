# ComponentOrderAssistant

## What it does now
Scrapes websites that sell electronic components (currently supports [Tayda](https://www.taydaelectronics.com/)) and
creates a local database of basic product information for local use.

## What it will do in the future
Allow users to set preferred products for each use case and generate .csv files for Tayda's "Quick Order" feature,
saving time and money when sourcing parts for a project.

### Example use case:
I am planning to build 10 guitar pedals and need to source parts. Given a list of materials for each pedal, I can
quickly check Tayda's selection and choose which resistors, capacitors, knobs, etc. I prefer.
Then I can simply generate a "quick order" .csv file to upload to Tayda instead of building my cart manually,
saving potentially hours of browsing and reducing the chance that I make a mistake in the quantity or forget to add
something.

## What I learned
- Used BeautifulSoup, Chrome dev tools, and CSS selectors to write algorithms that locate relevant product data
- Used SQLite3 to create a lightweight local database for storing product information