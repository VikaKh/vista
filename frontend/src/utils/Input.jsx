import React from 'react';
import { TextField } from '@mui/material';

const Input = (props) => {
    return (
        <TextField 
            onChange={(event)=> props.setValue(event.target.value)}
            value={props.value}
            label={props.label}
            type={props.type}
            variant="standard"
            placeholder={props.placeholder}
            fullWidth 
            required
            sx={{
                mb:"1rem"
            }}
            />
    );
};

export default Input;
