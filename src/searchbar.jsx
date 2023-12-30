import React, { useState, useEffect } from 'react';
import './Search.css';

const SearchBar = () => {
  const [query, setQuery] = useState('');
  // ... (rest of your component)

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log('Search submitted for:', query);

    // Make an HTTP POST request to your Flask server to get parking data
    try {
      const response = await fetch('/api/get_parking', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(query), // Send the query as JSON
      });

      if (response.ok) {
        const parkingData = await response.json();
        console.log('Parking data:', parkingData);

        // Handle the received parking data, e.g., update state or call a function to display the results
        // You can use the onSearch prop if you want to pass data to a parent component
        if (onSearch) {
          onSearch(parkingData);
        }
      } else {
        console.error('Failed to fetch parking data');
      }
    } catch (error) {
      console.error('Error fetching parking data:', error);
    }
  };





  return (
    <div className="search-container">
      <form onSubmit={handleSubmit}>
        <div className="bar">
          <div className="searchbar">
            <input
              type="text"
              value={query}
              onChange={handleInputChange}
              placeholder="Search Maps"
              className="search-input"
            />
            <button type="submit" className="search-button">
              <img
                src="https://cdn-icons-png.flaticon.com/512/1150/1150654.png"
                alt="Search Icon"
                style={{ height: '20px', position: 'relative', top: '5px' }}
              />
            </button>
          </div>
        </div>
      </form>

      {/* Conditionally render drop-down menu only when the search button is clicked and there is input */}
      {searchButtonClicked && query && (
        <div className="results-container">
          <ul>
            {autocompleteSuggestions
              .filter(suggestion =>
                suggestion.toLowerCase().startsWith(query.toLowerCase())
              )
              .slice(0, 5) // Limit the number of results to 5
              .map((result, index) => (
                <li key={index} className="result-item">
                  <span className="address">{result}</span>
                  {index < 4 && <div className="divider"></div>}
                </li>
              ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default SearchBar;


// import React, { useState, useEffect } from 'react';
// import './Search.css';

// const SearchBar = () => {
//   const [query, setQuery] = useState('');
//   const [autocompleteSuggestions, setAutocompleteSuggestions] = useState([]);
//   const [searchButtonClicked, setSearchButtonClicked] = useState(false);

//   useEffect(() => {
//     // Fetch data from output.txt or your API endpoint
//     fetch('/output.txt')
//       .then(response => response.text())
//       .then(data => {
//         // Split the data into an array of parking lot names
//         const suggestions = data.split('\n').filter(name => name.trim() !== '');
//         setAutocompleteSuggestions(suggestions);
  
//         // Log the content of autocompleteSuggestions
//         console.log('autocompleteSuggestions:', suggestions);
//       })
//       .catch(error => console.error('Error fetching data:', error));
//   }, []);

//   const handleInputChange = (event) => {
//     const inputValue = event.target.value;
//     setQuery(inputValue);
//   };

//   const handleSubmit = (event) => {
//     event.preventDefault();
//     console.log('Search submitted for:', query);

//     // Set the search button as clicked
//     setSearchButtonClicked(true);

//     // You can perform a search here or handle the form submission as needed
//   };

//   return (
//     <div className="search-container">
//       <form onSubmit={handleSubmit}>
//         <div className="bar">
//           <div className="searchbar">
//             <input
//               type="text"
//               value={query}
//               onChange={handleInputChange}
//               placeholder="Search Maps"
//               className="search-input"
//             />
//             <button type="submit" className="search-button">
//               <img
//                 src="https://cdn-icons-png.flaticon.com/512/1150/1150654.png"
//                 alt="Search Icon"
//                 style={{ height: '20px', position: 'relative', top: '5px' }}
//               />
//             </button>
//           </div>
//         </div>
//       </form>

//       {/* Conditionally render drop-down menu only when the search button is clicked and there is input */}
//       {searchButtonClicked && query && (
//         <div className="results-container">
//           <ul>
//             {autocompleteSuggestions
//               .filter(suggestion =>
//                 suggestion.toLowerCase().startsWith(query.toLowerCase())
//               )
//               .slice(0, 5) // Limit the number of results to 5
//               .map((result, index) => (
//                 <li key={index}>{result}</li>
//               ))}
//           </ul>
//         </div>
//       )}
//     </div>
//   );
// };

// export default SearchBar;

