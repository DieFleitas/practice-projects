import React, { SetStateAction, useState } from 'react';
import Layout from '../../Layout';
import { Box, InputAdornment, InputBase, Paper, Typography } from '@mui/material';
import SearchIcon from "../../assets/icons/icon-search.svg"

const Home = () => {
  const [search, setSearch] = useState('');
  const handleSearch = (e: { target: { value: SetStateAction<string> } }) => {
    setSearch(e.target.value);
  };
  return (
    <Layout>
      <Box>
        <Paper
          component="form"
          sx={{
            display: 'flex',
            alignItems: 'center',
            borderRadius: 'default',
            padding: 1,
            backgroundColor: '#10141f',
            border: 'none',
          }}
        >
          <InputBase
            placeholder="Search for movies or TV series"
            sx={{ marginLeft: 1, flex: 1, color: 'white', border: 'none' }}
            value={{ search }}
            onChange={handleSearch}
            startAdornment= {
              <InputAdornment position='start'>
                <img src={SearchIcon} alt="search icon" width={20} height={20} />
              </InputAdornment>
            }
          />
        </Paper>
      </Box>
      <Box py={2} px={4}>
            {search === "" ? (
              <Box width="100%">
                <Box width="100%">
                  <Typography variant='h5' component="h1" my={6} fontWeight={400}>
                    Trending
                  </Typography>
                  <MovieTrendList trendingList={trendingList} />
                </Box>
                <Box width="100%">
                  <Typography variant='h5' component="h1" my={6} fontWeight={400}>
                    Recommended for you
                  </Typography>
                  <MovieList recommendedList={recommendedList} />
                </Box>
              </Box>
            ) : (
              <Box width="100%">
                <Typography>Found</Typography>
              </Box>
            )}
      </Box>
    </Layout>
  );
};

export default Home;
