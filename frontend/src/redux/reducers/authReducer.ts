interface Bug {
  id: number;
  description: string;
  resolved: boolean;
}

interface State {
  bugs: Bug[];
  lastId: number;
}

const initialState: State = {
  bugs: [],
  lastId: 0,
};

function reducer(state: State = initialState, action: any): State {
  switch (action.type) {
    case "bugAdded":
      return {
        ...state,
        bugs: [
          ...state.bugs,
          {
            id: state.lastId + 1,
            description: action.payload.description,
            resolved: false,
          },
        ],
        lastId: state.lastId + 1,
      };
    default:
      return state;
  }
}
