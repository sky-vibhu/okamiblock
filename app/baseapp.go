package app

import (
	"errors"
	"io"
)

// Close will be called in graceful shutdown in start cmd
func (app *Okami) Close() error {
	err := app.BaseApp.Close()

	if cms, ok := app.CommitMultiStore().(io.Closer); ok {
		return errors.Join(err, cms.Close())
	}

	return err
}
