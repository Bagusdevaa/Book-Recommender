import react from 'react';

const BookCard = ({ book, onClick }) => {
    const truncateText = (text, maxWords = 20) => {
        if (!text) return 'No description available';
        const words = text.split(' ');
        return words.length > maxWords
            ? words.slice(0, maxWords).join(' ') + '...'
            : text;
    };
    const formatAuthors = (authors) => {
        if (!authors) return 'Unknown Author';
        // Handle multiple authors separated by semicolon
        const authorList = authors.split(';');
        if (authorList.length > 2) {
            return `${authorList[0]} and ${authorList.length - 1} others`;
        }
        return authorList.join(' & ');
    };

    return (
        <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-all duration-300 cursor-pointer overflow-hidden"
            onClick={() => onClick && onClick(book)}>
            {/* Book Cover */}
            <div className="relative h-48 bg-gray-100">
                {book.large_thumbnail && book.large_thumbnail !== 'cover-not-found.jpg' ? (
                    <img
                        src={book.large_thumbnail}
                        alt={book.title}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                            e.target.style.display = 'none';
                            e.target.nextSibling.style.display = 'flex';
                        }}
                    />
                ) : null}
                <div className="absolute inset-0 bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center text-gray-500"
                    style={{ display: book.large_thumbnail && book.large_thumbnail !== 'cover-not-found.jpg' ? 'none' : 'flex' }}>
                    <span className="text-2xl">📚</span>
                </div>
            </div>

            {/* Book Info */}
            <div className="p-4">
                <h3 className="font-semibold text-lg text-gray-800 mb-2 line-clamp-2 leading-tight">
                    {book.title}
                </h3>

                <p className="text-sm text-gray-600 mb-2">
                    by {formatAuthors(book.authors)}
                </p>

                <p className="text-sm text-gray-700 mb-3 line-clamp-3">
                    {truncateText(book.description, 15)}
                </p>

                {/* Rating and Category */}
                <div className="flex justify-between items-center text-xs text-gray-500 mb-2">
                    <span className="flex items-center">
                        ⭐ {book.average_rating ? book.average_rating.toFixed(1) : 'N/A'}
                    </span>

                    {book.simple_categories && book.simple_categories !== "" && (
                        <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">
                            {book.simple_categories}
                        </span>
                    )}
                </div>
            </div>
        </div>
    );
};

export default BookCard;


