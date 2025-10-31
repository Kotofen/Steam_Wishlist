import './Wishlist.css';

const TableBody = ({ tableData, columns }) => {
 return (
  <tbody>
   {tableData.map((data) => {
    return (
     <tr key={data.id}>
        <td><img src={data.image} /></td>
      {columns.map(({ accessor }) => {
       const tData = data[accessor] ? data[accessor] : "—";
       switch (accessor) {
        case 'game_name':
          return <td key={accessor}><a href={`https://store.steampowered.com/app/${data.id}`} target="_blank">{tData}</a></td>
        case 'discount':
          return <td key={accessor}><div class='discount'>{tData}%</div></td>
        default:
          return <td key={accessor}>{tData}</td>;
       }
      })} 
     </tr>
    );
   })}
  </tbody>
 );
};

export default TableBody;