import React from 'react';
import { useState, useEffect, createContext, useContext } from 'react';
import './Wishlist.css';
import TableHead from './TableHead';
import TableBody from './TableBody';


function Change_UserID({ onButtonPress }) {
  const [UserID, setUserID] = useState('');
  const { wishlist, fetchWishlist } = useContext(WishlistContext)

  const handleUserIDChange = (event) => {
    setUserID(event.target.value);
  };



  const handleSubmit = () => {
    onButtonPress(UserID);
  };

  return (
    <div class="chng_uid_block">
      <p class="text-uid">Enter Steam UserID:</p>
      <input
        type="text"
        value={UserID}
        onChange={handleUserIDChange}
        placeholder="Steam UserID"
      />
      <button class="button-1" onClick={handleSubmit}>Change UserID</button>
    </div>
  );
}

const WishlistContext = createContext({
  wishlist: [], fetchWishlist: () => { }
})

export default function Show_Wishlist() {
  const [wishlist, setWishlist] = useState([]);
  const [uid, setUserID] = useState([])

  const updateUID = (newUID) => {
    setUserID(newUID);
    setWishlist([])
    fetchWishlist(newUID)
  }

  const fetchWishlist = async (fetchedUid = uid) => {
    try {
      const kfc = await fetch(`${process.env.REACT_APP_BACKEND_URL}/get_wishlist_size?userid=${fetchedUid}`, {
        method: "GET",
        headers: {
          'Content-Type': 'application/json',
        },
      })
      const wishlist_length = (await kfc.json()).data
      for (let i = 0; i < wishlist_length; i += 5) {
        let end
        if (i + 5 < wishlist_length) {
          end = i + 5
        } else { end = wishlist_length }
        const get_wishlist_part = await fetch(`${process.env.REACT_APP_BACKEND_URL}/get_wishlist_games?userid=${fetchedUid}&start=${i}&end=${end}`, {
          method: "GET",
          headers: {
            'Content-Type': 'application/json',
          },
        })
        const wishlist_part = (await get_wishlist_part.json())

        setWishlist(w => [...w, ...wishlist_part])
      }
    } catch {
      alert("Enter UserID to fetch wishlist.");
    }
    //setWishlist(data.games);
  }

  useEffect(() => {
    fetchWishlist()
  }, []);

  const columns = [
    { label: "Game Name", accessor: "game_name" },
    { label: "Description", accessor: "description" },
    { label: "Price Kazakhstan", accessor: "price_kz" },
    { label: "Price Russia", accessor: "price_ru" },
    { label: "Discount", accessor: "discount" },
  ];

  const handleSorting = (sortField, sortOrder) => {
    if (sortField) {
      const sorted = [...wishlist].sort((a, b) => {
        return (
          a[sortField].toString().localeCompare(b[sortField].toString(), "en", {
            numeric: true,
          }) * (sortOrder === "asc" ? 1 : -1)
        );
      });
      setWishlist(sorted);
    }
  };

  return (
    <React.Fragment>
      <WishlistContext.Provider value={{ wishlist, fetchWishlist }}>
        <Change_UserID onButtonPress={updateUID} />
        <div class="wishlist">
          <table class="wishlist-table">
            <TableHead columns={columns} handleSorting={handleSorting} />
            <TableBody columns={columns} tableData={wishlist} />
          </table>
        </div>
      </WishlistContext.Provider>
    </React.Fragment>
  );
};
